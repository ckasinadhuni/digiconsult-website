#!/usr/bin/env python3

"""
Manual Test AI Workflow - Direct deployment with working API endpoints
"""

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

# Simple working AI workflow
manual_test_workflow = {
    "name": f"🧪 Manual Test AI - {datetime.now().strftime('%H:%M:%S')}",
    "nodes": [
        {
            "parameters": {},
            "id": "manual-trigger",
            "name": "Manual Trigger",
            "type": "@n8n/n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [200, 300]
        },
        {
            "parameters": {
                "values": {
                    "string": [
                        {
                            "name": "message",
                            "value": "Hello AI! Please help me with a simple task."
                        }
                    ]
                }
            },
            "id": "input-data",
            "name": "Input Data",
            "type": "@n8n/n8n-nodes-base.set",
            "typeVersion": 3.3,
            "position": [400, 300]
        },
        {
            "parameters": {
                "method": "POST",
                "url": f"{config['local_services']['ollama']}/api/generate",
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "model", "value": "mistral:7b"},
                        {"name": "prompt", "value": "You are a helpful AI assistant. User says: {{ $json.message }}. Please respond helpfully."},
                        {"name": "stream", "value": False}
                    ]
                },
                "options": {
                    "bodyContentType": "json"
                }
            },
            "id": "ai-call",
            "name": "AI Call",
            "type": "@n8n/n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [600, 300]
        }
    ],
    "connections": {
        "Manual Trigger": {
            "main": [[{"node": "Input Data", "type": "main", "index": 0}]]
        },
        "Input Data": {
            "main": [[{"node": "AI Call", "type": "main", "index": 0}]]
        }
    },
    "settings": {}
}

print("🧪 DEPLOYING MANUAL TEST AI WORKFLOW...")

try:
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=manual_test_workflow,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        workflow_info = response.json()
        workflow_id = workflow_info.get('id')
        print(f"✅ MANUAL TEST AI DEPLOYED!")
        print(f"🆔 Workflow ID: {workflow_id}")
        print(f"🌐 View: {config['base_url']}/workflow/{workflow_id}")
        print()
        print("🧪 TESTING INSTRUCTIONS:")
        print(f"1. Go to: {config['base_url']}/workflow/{workflow_id}")
        print("2. Click 'Execute Workflow' button")
        print("3. Check output in 'AI Call' node")
        print("4. Verify AI response is generated")
        
    else:
        print(f"❌ Deployment failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")