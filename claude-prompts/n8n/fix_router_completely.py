#!/usr/bin/env python3

"""
Fix router completely - remove conflicting old rules format
"""

import json
import requests

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    headers = {'X-N8N-API-KEY': config['api_key']}
    workflow_id = 'jyskZP1sldP7NwYA'
    
    print("🔧 FIXING ROUTER COMPLETELY")
    print("=" * 40)
    
    # Get workflow
    response = requests.get(f"{config['base_url']}/api/v1/workflows/{workflow_id}", headers=headers)
    workflow = response.json()
    
    # Find router node
    router = None
    for node in workflow['nodes']:
        if 'router' in node['name'].lower() or node['type'] == 'n8n-nodes-base.switch':
            router = node
            break
    
    print(f"Current router parameters keys: {list(router['parameters'].keys())}")
    
    # COMPLETELY REBUILD router parameters - remove old rules format
    router['parameters'] = {
        "conditions": {
            "options": {
                "caseSensitive": False, 
                "leftValue": "", 
                "typeValidation": "strict"
            },
            "conditions": [
                {
                    "leftValue": "={{ $json.message.text }}",
                    "operator": {
                        "type": "string", 
                        "operation": "startsWith", 
                        "rightValue": "/search"
                    }
                },
                {
                    "leftValue": "={{ $json.message.text }}",
                    "operator": {
                        "type": "string", 
                        "operation": "startsWith", 
                        "rightValue": "/files"
                    }
                },
                {
                    "leftValue": "={{ $json.message.voice }}",
                    "operator": {
                        "type": "object", 
                        "operation": "exists"
                    }
                },
                {
                    "leftValue": "={{ $json.message.photo }}",
                    "operator": {
                        "type": "array", 
                        "operation": "notEmpty"
                    }
                },
                {
                    "leftValue": "={{ $json.message.document }}",
                    "operator": {
                        "type": "object", 
                        "operation": "exists"
                    }
                },
                {
                    "leftValue": "={{ $json.message.text }}",
                    "operator": {
                        "type": "string", 
                        "operation": "exists"
                    }
                }
            ],
            "combinator": "or"
        }
    }
    
    print("✅ Rebuilt router with clean conditions (no old rules)")
    print(f"   Conditions: {len(router['parameters']['conditions']['conditions'])}")
    
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
        print("✅ Router fixed successfully!")
        print("🧪 Test the workflow now - should work without a.ok(to) error")
    else:
        print(f"❌ Update failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()