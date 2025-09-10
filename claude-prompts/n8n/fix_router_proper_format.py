#!/usr/bin/env python3

"""
Fix router with proper n8n Switch node format
Using rules.values structure, not conditions
"""

import json
import requests

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    headers = {'X-N8N-API-KEY': config['api_key']}
    workflow_id = 'jyskZP1sldP7NwYA'
    
    print("🔧 FIXING ROUTER WITH CORRECT N8N FORMAT")
    print("=" * 50)
    
    # Get workflow
    response = requests.get(f"{config['base_url']}/api/v1/workflows/{workflow_id}", headers=headers)
    workflow = response.json()
    
    # Find router node
    router = None
    for node in workflow['nodes']:
        if 'router' in node['name'].lower() or node['type'] == 'n8n-nodes-base.switch':
            router = node
            break
    
    # Use correct n8n Switch node format: rules.values
    router['parameters'] = {
        "mode": "rules",
        "rules": {
            "values": [
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json.message.text }}",
                                "rightValue": "/search",
                                "operator": {"type": "string", "operation": "startsWith"}
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "search_command"
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json.message.text }}",
                                "rightValue": "/files",
                                "operator": {"type": "string", "operation": "startsWith"}
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "files_command"
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json.message.voice }}",
                                "rightValue": "",
                                "operator": {"type": "object", "operation": "exists"}
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "voice_message"
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json.message.photo }}",
                                "rightValue": "",
                                "operator": {"type": "array", "operation": "notEmpty"}
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "photo_message"
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json.message.document }}",
                                "rightValue": "",
                                "operator": {"type": "object", "operation": "exists"}
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "document_message"
                }
            ]
        }
    }
    
    print("✅ Router configured with proper n8n rules.values format")
    print(f"   Rules count: {len(router['parameters']['rules']['values'])}")
    
    # Fix connections - router should have 5 outputs (5 rules)
    connections = workflow.get('connections', {})
    router_name = router['name']
    
    # Create 5 outputs for 5 rules
    router_outputs = []
    input_processor_name = "Enhanced Input Processor"
    
    for i in range(5):  # 5 rules = 5 outputs
        router_outputs.append([{"node": input_processor_name, "type": "main", "index": 0}])
    
    connections[router_name] = {"main": router_outputs}
    
    print(f"🔗 Fixed connections: {len(router_outputs)} outputs")
    
    # Update workflow
    clean_workflow = {
        "name": workflow["name"],
        "nodes": workflow["nodes"], 
        "connections": workflow["connections"],
        "settings": workflow.get("settings", {})
    }
    
    response = requests.put(
        f"{config['base_url']}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json=clean_workflow
    )
    
    if response.status_code == 200:
        print("✅ Router fixed with proper n8n format!")
        print("🧪 Router now has 5 rules with proper routing")
        print("📋 Rules:")
        print("  0: /search commands")
        print("  1: /files commands")
        print("  2: Voice messages") 
        print("  3: Photo messages")
        print("  4: Document messages")
    else:
        print(f"❌ Update failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()