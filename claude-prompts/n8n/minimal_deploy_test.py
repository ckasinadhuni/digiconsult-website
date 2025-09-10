#!/usr/bin/env python3

import json
import requests
from datetime import datetime

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

headers = {
    "X-N8N-API-KEY": config["api_key"],
    "Content-Type": "application/json"
}

# Create minimal working workflow
minimal_workflow = {
    "name": f"Claude CLI Test - {datetime.now().strftime('%H:%M:%S')}",
    "nodes": [
        {
            "parameters": {},
            "id": "start-node",
            "name": "Manual Trigger",
            "type": "@n8n/n8n-nodes-base.manualTrigger",
            "typeVersion": 1.1,
            "position": [240, 300]
        },
        {
            "parameters": {
                "jsCode": "return [{\n  json: {\n    message: 'Claude CLI workflow deployed successfully!',\n    timestamp: new Date().toISOString(),\n    contextEngineering: 'enabled',\n    deployment: 'successful'\n  }\n}];"
            },
            "id": "success-node", 
            "name": "Success Message",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [460, 300]
        }
    ],
    "connections": {
        "Manual Trigger": {
            "main": [[{"node": "Success Message", "type": "main", "index": 0}]]
        }
    },
    "settings": {
        "executionOrder": "v1"
    },
    "staticData": {},
    "pinData": {},
    "tags": ["claude-cli", "test", "deployed"],
    "triggerCount": 1,
    "active": False
}

print("🔄 Deploying minimal test workflow...")

try:
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=minimal_workflow,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        workflow_info = response.json()
        workflow_id = workflow_info.get('id')
        print(f"✅ Workflow deployed! ID: {workflow_id}")
        
        # Auto-activate
        activate_response = requests.patch(
            f"{config['base_url']}/api/v1/workflows/{workflow_id}",
            headers=headers,
            json={"active": True}
        )
        
        if activate_response.status_code == 200:
            print("✅ Workflow activated!")
            print(f"🌐 View in n8n UI: {config['base_url']}/workflow/{workflow_id}")
            print(f"📋 Check 'My workflows': {config['base_url']}/workflows")
        else:
            print(f"⚠️ Activation failed: {activate_response.status_code}")
        
    else:
        print(f"❌ Deployment failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")