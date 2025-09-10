#!/usr/bin/env python3

"""
Fix router with actual Telegram data structure
The data comes as an array: [{"update_id": ..., "message": {...}}]
"""

import json
import requests

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    headers = {'X-N8N-API-KEY': config['api_key']}
    workflow_id = 'jyskZP1sldP7NwYA'
    
    print("🔧 FIXING ROUTER WITH ACTUAL TELEGRAM DATA STRUCTURE")
    print("=" * 60)
    
    # Test data structure
    telegram_data = [
        {
            "update_id": 360738392,
            "message": {
                "message_id": 170,
                "from": {
                    "id": 6778059024,
                    "is_bot": False,
                    "first_name": "CK",
                    "last_name": "Kasi",
                    "language_code": "en"
                },
                "chat": {
                    "id": 6778059024,
                    "first_name": "CK",
                    "last_name": "Kasi",
                    "type": "private"
                },
                "date": 1755703300,
                "text": "Hello"
            }
        }
    ]
    
    print("📋 ACTUAL TELEGRAM DATA STRUCTURE:")
    print("- Data is an ARRAY")
    print("- Message is at $json[0].message")
    print("- Text is at $json[0].message.text")
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
    
    # CORRECT router parameters with proper data paths
    router['parameters'] = {
        "mode": "rules",
        "rules": {
            "values": [
                {
                    "conditions": {
                        "options": {"caseSensitive": False},
                        "conditions": [
                            {
                                "leftValue": "={{ $json[0].message.text }}",  # CORRECT: Array access
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
                                "leftValue": "={{ $json[0].message.text }}",  # CORRECT: Array access
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
                                "leftValue": "={{ $json[0].message.voice }}",  # CORRECT: Array access
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
                                "leftValue": "={{ $json[0].message.photo }}",  # CORRECT: Array access
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
                                "leftValue": "={{ $json[0].message.document }}",  # CORRECT: Array access
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
                                "leftValue": "={{ $json[0].message.text }}",  # CORRECT: Array access
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
    
    print("✅ Updated router with CORRECT data paths:")
    print("  - $json[0].message.text (was: $json.message.text)")
    print("  - $json[0].message.voice (was: $json.message.voice)")
    print("  - $json[0].message.photo (was: $json.message.photo)")
    print("  - $json[0].message.document (was: $json.message.document)")
    print()
    print("📋 Router now has 6 rules (added text fallback)")
    
    # Update workflow
    clean_workflow = {
        "name": workflow["name"],
        "nodes": workflow["nodes"], 
        "connections": workflow["connections"],
        "settings": workflow.get("settings", {})
    }
    
    # Fix connections for 6 rules
    router_name = router['name']
    router_outputs = []
    input_processor_name = "Enhanced Input Processor"
    
    for i in range(6):  # 6 rules = 6 outputs
        router_outputs.append([{"node": input_processor_name, "type": "main", "index": 0}])
    
    clean_workflow["connections"][router_name] = {"main": router_outputs}
    
    print("🔗 Updated connections: 6 outputs for 6 rules")
    
    response = requests.put(
        f"{config['base_url']}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json=clean_workflow
    )
    
    if response.status_code == 200:
        print("\\n✅ Router fixed with correct Telegram data structure!")
        print("🧪 Test with: 'Hello', '/search test', voice message, photo")
        print("📋 No more a.ok(to) errors - router accesses correct array index")
    else:
        print(f"\\n❌ Update failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()