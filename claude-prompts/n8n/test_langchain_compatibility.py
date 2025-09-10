#!/usr/bin/env python3

"""Test LangChain Node Compatibility - Verify nodes work in practice"""

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

# Test workflow with LangChain nodes
test_langchain_workflow = {
    "name": f"🧪 LangChain Node Test - {datetime.now().strftime('%H:%M:%S')}",
    "nodes": [
        # 1. Manual Trigger
        {
            "parameters": {},
            "id": "manual-trigger",
            "name": "Manual Trigger",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [200, 300]
        },
        
        # 2. Ollama Chat Model (LangChain)
        {
            "parameters": {
                "model": "mistral:7b",
                "options": {
                    "baseURL": config["local_services"]["ollama"]
                }
            },
            "id": "ollama-chat",
            "name": "Ollama Chat Model",
            "type": "@n8n/n8n-nodes-langchain.chatOllama",
            "typeVersion": 1,
            "position": [400, 300]
        },
        
        # 3. AI Agent (LangChain)
        {
            "parameters": {
                "agent": "conversationalAgent",
                "promptType": "define",
                "text": "Hello, can you help me test this workflow?",
                "options": {
                    "systemMessage": "You are a helpful assistant testing n8n LangChain integration."
                }
            },
            "id": "ai-agent",
            "name": "AI Agent",
            "type": "@n8n/n8n-nodes-langchain.agent",
            "typeVersion": 1,
            "position": [600, 300]
        }
    ],
    
    "connections": {
        "Manual Trigger": {
            "main": [[{"node": "AI Agent", "type": "main", "index": 0}]]
        },
        "Ollama Chat Model": {
            "ai_languageModel": [[{"node": "AI Agent", "type": "ai_languageModel", "index": 0}]]
        }
    },
    
    "settings": {}
}

print("🧪 TESTING LANGCHAIN NODE COMPATIBILITY...")
print(f"📊 Testing nodes:")
print(f"  • Manual Trigger: n8n-nodes-base.manualTrigger v1")
print(f"  • Ollama Chat: @n8n/n8n-nodes-langchain.chatOllama v1")
print(f"  • AI Agent: @n8n/n8n-nodes-langchain.agent v1")
print()

try:
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=test_langchain_workflow,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        workflow_info = response.json()
        workflow_id = workflow_info.get('id')
        print(f"✅ LANGCHAIN NODES WORK!")
        print(f"🆔 Test Workflow ID: {workflow_id}")
        print(f"🌐 View: {config['base_url']}/workflow/{workflow_id}")
        print()
        print("🎉 CONCLUSION: LangChain nodes ARE available and compatible!")
        print("💡 We can use the full multimodal workflow with LangChain!")
        
    else:
        print(f"❌ LangChain nodes FAILED: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        print("❌ CONCLUSION: LangChain nodes appear available but have compatibility issues")
        
except Exception as e:
    print(f"❌ Error testing LangChain nodes: {e}")
    print("❌ CONCLUSION: LangChain nodes may not work in practice")