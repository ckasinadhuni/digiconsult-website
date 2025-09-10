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

# Get existing workflow structure to copy exact format
response = requests.get(f"{config['base_url']}/api/v1/workflows", headers=headers)
existing_workflows = response.json().get('data', [])

if existing_workflows:
    template = existing_workflows[0]
    
    # Create new workflow using exact same structure
    new_workflow = {
        "name": f"Claude CLI Working Test - {datetime.now().strftime('%H:%M:%S')}",
        "active": False,
        "connections": {},
        "meta": template.get("meta"),
        "nodes": [
            {
                "parameters": {},
                "id": "claude-test-trigger",
                "name": "Start Test",
                "type": "@n8n/n8n-nodes-base.manualTrigger", 
                "typeVersion": 1,
                "position": [200, 300]
            }
        ],
        "pinData": {},
        "settings": template.get("settings", {}),
        "staticData": template.get("staticData"),
        "tags": ["claude-cli", "working"],
        "triggerCount": 1,
        "versionId": template.get("versionId", "")
    }
    
    print("🔄 Deploying workflow with exact template structure...")
    
    try:
        deploy_response = requests.post(
            f"{config['base_url']}/api/v1/workflows",
            headers=headers,
            json=new_workflow,
            timeout=30
        )
        
        if deploy_response.status_code in [200, 201]:
            workflow_info = deploy_response.json()
            workflow_id = workflow_info.get('id')
            print(f"✅ SUCCESS! Workflow deployed with ID: {workflow_id}")
            print(f"🌐 View at: {config['base_url']}/workflow/{workflow_id}")
            print(f"📋 Check 'My workflows': {config['base_url']}/workflows")
            
            # Activate it
            activate = requests.patch(
                f"{config['base_url']}/api/v1/workflows/{workflow_id}",
                headers=headers,
                json={"active": True}
            )
            
            if activate.status_code == 200:
                print("✅ Workflow activated and ready to test!")
            
        else:
            print(f"❌ Failed: {deploy_response.status_code}")
            print(f"Response: {deploy_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ No existing workflows found to use as template")