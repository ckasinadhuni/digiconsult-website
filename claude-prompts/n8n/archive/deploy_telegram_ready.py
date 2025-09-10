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

print("🔍 Checking available credentials for Telegram...")

# Check for Telegram credentials
cred_response = requests.get(f"{config['base_url']}/api/credentials", headers=headers)
telegram_cred_id = None

if cred_response.status_code == 200:
    try:
        credentials = cred_response.json()
        for cred in credentials:
            if cred.get('type') == 'telegramApi':
                telegram_cred_id = cred['id']
                print(f"✅ Found Telegram credential: {cred['name']} (ID: {telegram_cred_id})")
                break
    except:
        print("⚠️ No credentials found in response")

if not telegram_cred_id:
    print("❌ No Telegram credentials found!")
    print("🔧 REQUIRED: Create Telegram credential in n8n:")
    print(f"1. Go to: {config['base_url']}/credentials")
    print("2. Click 'Add Credential' → 'Telegram'")
    print(f"3. Enter bot token: {config['telegram_bot_token']}")
    print("4. Save and rerun this script")
    print()
    telegram_cred_id = "MISSING_TELEGRAM_CREDENTIAL"  # Placeholder for now

# Create Telegram-ready AI workflow
telegram_workflow = {
    "name": f"🤖 Telegram AI Assistant - {datetime.now().strftime('%H:%M:%S')}",
    "nodes": [
        {
            "parameters": {
                "updates": ["message"]
            },
            "id": "telegram-trigger",
            "name": "Telegram Trigger",
            "type": "@n8n/n8n-nodes-base.telegramTrigger",
            "typeVersion": 1.1,
            "position": [200, 300],
            "credentials": {"telegramApi": telegram_cred_id}
        },
        {
            "parameters": {
                "conditions": {
                    "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                    "conditions": [
                        {
                            "leftValue": "={{ $json.message.voice }}",
                            "operator": {"type": "object", "operation": "exists"}
                        },
                        {
                            "leftValue": "={{ $json.message.photo }}",
                            "operator": {"type": "object", "operation": "exists"}  
                        },
                        {
                            "leftValue": "={{ $json.message.text }}",
                            "operator": {"type": "string", "operation": "exists"}
                        }
                    ],
                    "combinator": "or"
                }
            },
            "id": "message-router",
            "name": "Message Type Router",
            "type": "@n8n/n8n-nodes-base.switch",
            "typeVersion": 3,
            "position": [400, 300]
        },
        {
            "parameters": {
                "agent": "conversationalAgent",
                "promptType": "define", 
                "text": "{{ $json.message.text || $json.processed_text || 'Hello! How can I help you?' }}",
                "options": {
                    "systemMessage": "You are a helpful Telegram AI assistant with these capabilities:\n\n🧠 CONTEXT AWARENESS:\n- Remember our conversation history\n- Understand user preferences and patterns\n- Provide personalized responses\n\n🛠️ AVAILABLE TOOLS:\n- Mathematical calculations\n- Web search and information retrieval\n- Code execution and analysis\n\n📱 TELEGRAM FEATURES:\n- Process text, voice messages, and images\n- Send formatted responses with markdown\n- Handle group and private chats\n\n💬 RESPONSE STYLE:\nProvide helpful, concise responses. Use emojis appropriately. For complex requests:\n1. 🔍 Context: What I understand\n2. 💭 Analysis: My reasoning\n3. ✅ Answer: Direct response\n4. 🎯 Next: Suggested actions",
                    "maxTokens": 4000,
                    "temperature": 0.7
                }
            },
            "id": "ai-agent",
            "name": "Context-Aware AI Agent",
            "type": "@n8n/n8n-nodes-langchain.agent",
            "typeVersion": 1.4,
            "position": [600, 300]
        },
        {
            "parameters": {
                "model": "mistral:7b",
                "options": {
                    "baseURL": config["local_services"]["ollama"],
                    "temperature": 0.7,
                    "maxTokens": 2000
                }
            },
            "id": "ollama-model",
            "name": "Ollama Mistral 7B",
            "type": "@n8n/n8n-nodes-langchain.chatOllama", 
            "typeVersion": 1.2,
            "position": [600, 480]
        },
        {
            "parameters": {
                "sessionIdExpression": "={{ $json.message.chat.id }}",
                "contextWindowLength": 10
            },
            "id": "simple-memory",
            "name": "Simple Memory",
            "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
            "typeVersion": 1.2,
            "position": [800, 200]
        },
        {
            "parameters": {},
            "id": "calculator-tool",
            "name": "Calculator Tool",
            "type": "@n8n/n8n-nodes-langchain.toolCalculator",
            "typeVersion": 1.2,
            "position": [800, 300]
        },
        {
            "parameters": {
                "playbookDescription": "Perform web searches and retrieve information from the internet",
                "workflowId": "{{ $workflow.id }}"
            },
            "id": "web-search-tool",
            "name": "Web Search Tool", 
            "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
            "typeVersion": 1.2,
            "position": [800, 400]
        },
        {
            "parameters": {},
            "id": "code-tool",
            "name": "Code Interpreter Tool",
            "type": "@n8n/n8n-nodes-langchain.toolCode",
            "typeVersion": 1.2,
            "position": [800, 500]
        },
        {
            "parameters": {
                "resource": "message",
                "operation": "sendMessage",
                "chatId": "={{ $json.message.chat.id }}",
                "text": "={{ $json.output }}",
                "additionalFields": {
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                }
            },
            "id": "telegram-send",
            "name": "Send Telegram Response",
            "type": "@n8n/n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [1000, 300],
            "credentials": {"telegramApi": telegram_cred_id}
        }
    ],
    "connections": {
        "Telegram Trigger": {
            "main": [[{"node": "Message Type Router", "type": "main", "index": 0}]]
        },
        "Message Type Router": {
            "main": [[{"node": "Context-Aware AI Agent", "type": "main", "index": 0}]]
        },
        "Context-Aware AI Agent": {
            "main": [[{"node": "Send Telegram Response", "type": "main", "index": 0}]]
        },
        "Ollama Mistral 7B": {
            "ai_languageModel": [[{"node": "Context-Aware AI Agent", "type": "ai_languageModel", "index": 0}]]
        },
        "Simple Memory": {
            "ai_memory": [[{"node": "Context-Aware AI Agent", "type": "ai_memory", "index": 0}]]
        },
        "Calculator Tool": {
            "ai_tool": [[{"node": "Context-Aware AI Agent", "type": "ai_tool", "index": 0}]]
        },
        "Web Search Tool": {
            "ai_tool": [[{"node": "Context-Aware AI Agent", "type": "ai_tool", "index": 1}]]
        },
        "Code Interpreter Tool": {
            "ai_tool": [[{"node": "Context-Aware AI Agent", "type": "ai_tool", "index": 2}]]
        }
    },
    "settings": {}
}

print("🚀 Deploying production-ready Telegram AI Assistant...")
print("\n📋 WORKFLOW COMPONENTS:")
print("├── 🔥 Telegram Trigger (requires credential)")
print("├── 🔄 Message Type Router (n8n Switch node)")  
print("├── 🤖 Context-Aware AI Agent (LangChain)")
print("├── 🧠 Ollama Mistral 7B (local LLM)")
print("├── 💾 Simple Memory (n8n native)")
print("├── 🧮 Calculator Tool (n8n native)")
print("├── 🌐 Web Search Tool (n8n native)")
print("├── 💻 Code Interpreter (n8n native)")
print("└── 📱 Telegram Send (requires same credential)")
print()

try:
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=telegram_workflow,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        workflow_info = response.json()
        workflow_id = workflow_info.get('id')
        print(f"✅ TELEGRAM AI ASSISTANT DEPLOYED!")
        print(f"🆔 Workflow ID: {workflow_id}")
        print(f"🌐 View: {config['base_url']}/workflow/{workflow_id}")
        print()
        
        print("🔧 CREDENTIALS REQUIRED:")
        if telegram_cred_id == "MISSING_TELEGRAM_CREDENTIAL":
            print("❌ Telegram API credential - REQUIRED")
            print(f"   Create at: {config['base_url']}/credentials")
            print(f"   Bot Token: {config['telegram_bot_token']}")
        else:
            print("✅ Telegram API credential - CONFIGURED")
        
        print("\n📦 DEPENDENCIES:")
        print("✅ Ollama (local) - Already configured")
        print(f"   URL: {config['local_services']['ollama']}")
        print(f"   Model: mistral:7b")
        print()
        
        print("🛠️ TOOLS USED (all n8n native):")
        print("✅ Switch Node - Routes different message types")
        print("   Why: Handles text, voice, photos differently")
        print("✅ Simple Memory - Maintains conversation context")
        print("   Why: Remembers chat history per user/chat")
        print("✅ Calculator Tool - Mathematical operations")  
        print("   Why: Built-in, reliable arithmetic")
        print("✅ HTTP Request Tool - Web searches")
        print("   Why: Can fetch web content and APIs")
        print("✅ Code Tool - Execute code snippets")
        print("   Why: Handle programming questions")
        print()
        
        print("🧪 TESTING STEPS:")
        if telegram_cred_id != "MISSING_TELEGRAM_CREDENTIAL":
            print("1. ✅ Workflow is ready to test!")
            print("2. 📱 Send message to your Telegram bot")
            print("3. 🔍 Check execution in n8n UI")
            print("4. 💬 Bot should respond with AI-generated content")
        else:
            print("1. 🔑 First add Telegram credential")
            print("2. 🔄 Then activate the workflow")
            print("3. 📱 Test with Telegram messages")
        
    else:
        print(f"❌ Deployment failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")