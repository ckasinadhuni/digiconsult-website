#!/usr/bin/env python3

"""
Test Switch node formats by creating minimal workflows
"""

import json
import requests

def test_switch_formats():
    with open('config.json', 'r') as f:
        config = json.load(f)

    headers = {'X-N8N-API-KEY': config['api_key']}
    
    print("🧪 TESTING SWITCH NODE FORMATS")
    print("=" * 40)
    
    # Get available node types to see Switch node structure
    response = requests.get(f"{config['base_url']}/types/nodes.json")
    
    if response.status_code == 200:
        nodes = response.json()
        
        # Find Switch node
        switch_node = None
        for node in nodes:
            if node.get('name') == 'n8n-nodes-base.switch':
                switch_node = node
                break
        
        if switch_node:
            print("📋 SWITCH NODE FOUND:")
            print(f"Name: {switch_node.get('name')}")
            print(f"Display Name: {switch_node.get('displayName')}")
            print(f"Version: {switch_node.get('version')}")
            
            # Check for properties/parameters structure
            props = switch_node.get('properties', [])
            print(f"Properties count: {len(props)}")
            
            for prop in props[:5]:  # Show first 5 properties
                print(f"  - {prop.get('name', '?')}: {prop.get('type', '?')}")
                if prop.get('name') == 'rules':
                    print(f"    Rules structure: {json.dumps(prop, indent=4)[:200]}...")
        else:
            print("❌ Switch node not found")
    else:
        print(f"Failed to get node types: {response.status_code}")
    
    # Test actual Telegram data structure from current workflow
    print("\n📱 TESTING TELEGRAM DATA STRUCTURE:")
    
    # Create a simple test workflow to see Telegram structure
    test_workflow = {
        "name": "🧪 Telegram Data Test",
        "nodes": [
            {
                "parameters": {"updates": ["message"]},
                "id": "telegram-test",
                "name": "Telegram Test",
                "type": "n8n-nodes-base.telegramTrigger",
                "typeVersion": 1.2,
                "position": [200, 300],
                "credentials": {"telegramApi": "Nn48haw1evoNGuWO"}
            },
            {
                "parameters": {
                    "rules": {
                        "values": [
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
                                "renameOutput": true,
                                "outputKey": "text_message"
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
                                "renameOutput": true,
                                "outputKey": "photo_message"
                            }
                        ]
                    }
                },
                "id": "switch-test",
                "name": "Switch Test",
                "type": "n8n-nodes-base.switch",
                "typeVersion": 3,
                "position": [400, 300]
            }
        ],
        "connections": {
            "Telegram Test": {
                "main": [["Switch Test"]]
            }
        },
        "settings": {}
    }
    
    print("📤 Deploying test workflow...")
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=test_workflow
    )
    
    if response.status_code in [200, 201]:
        test_id = response.json()['id']
        print(f"✅ Test workflow created: {test_id}")
        print(f"🌐 View: {config['base_url']}/workflow/{test_id}")
        print("\nSend a test message to your Telegram bot to see the data structure!")
        
        return test_id
    else:
        print(f"❌ Test workflow failed: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    test_switch_formats()