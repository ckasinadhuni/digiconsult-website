#!/usr/bin/env python3

"""
Fix router with simple approach based on official Telegram API and n8n examples
Using direct $json.message paths, no transformations
"""

import json
import requests

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    headers = {'X-N8N-API-KEY': config['api_key']}
    workflow_id = 'jyskZP1sldP7NwYA'
    
    print("🔧 FIXING ROUTER - SIMPLE APPROACH")
    print("=" * 40)
    print("✅ Using direct $json.message paths")
    print("✅ Based on official Telegram API structure") 
    print("✅ Matches n8n multimodal examples")
    print()
    
    # Get workflow
    response = requests.get(f"{config['base_url']}/api/v1/workflows/{workflow_id}", headers=headers)
    workflow = response.json()
    
    # Find router node
    router = None
    for node in workflow['nodes']:
        if 'router' in node['name'].lower() or node['type'] == 'n8n-nodes-base.switch':
            router = node
            break
    
    print(f"🔍 Found router: {router['name']}")
    
    # Simple, clean router configuration
    router['parameters'] = {
        "mode": "rules",
        "rules": {
            "values": [
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
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json.message.text }}",
                                "rightValue": "/",
                                "operator": {"type": "string", "operation": "startsWith"}
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "command_message"
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json.message.text }}",
                                "rightValue": "",
                                "operator": {"type": "string", "operation": "exists"}
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "text_message"
                }
            ]
        }
    }
    
    print("📋 Router configured with 5 simple rules:")
    print("  1. Voice message - $json.message.voice exists")
    print("  2. Photo message - $json.message.photo not empty")
    print("  3. Document message - $json.message.document exists") 
    print("  4. Command message - $json.message.text starts with '/'")
    print("  5. Text message - $json.message.text exists (fallback)")
    print()
    
    # Fix connections for 5 rules
    router_name = router['name']
    router_outputs = []
    input_processor_name = "Enhanced Input Processor"
    
    for i in range(5):  # 5 rules = 5 outputs
        router_outputs.append([{"node": input_processor_name, "type": "main", "index": 0}])
    
    workflow["connections"][router_name] = {"main": router_outputs}
    
    print("🔗 Updated connections: 5 outputs for 5 rules")
    
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
        print("\n✅ Router fixed with simple approach!")
        print("🧪 Test with:")
        print("  • 'Hello' (text)")
        print("  • '/search test' (command)")
        print("  • Voice message")
        print("  • Photo")
        print("  • Document")
        print("\n📋 Should route correctly without a.ok(to) errors")
    else:
        print(f"\n❌ Update failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()