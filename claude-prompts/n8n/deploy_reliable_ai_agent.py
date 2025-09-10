#!/usr/bin/env python3

"""
Reliable AI Agent - Using validated LangChain nodes with local Mistral 7B
Most reliable proven approach
"""

import json
import requests
from datetime import datetime
from template_validator import TemplateValidator

def main():
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)

    headers = {
        "X-N8N-API-KEY": config["api_key"],
        "Content-Type": "application/json"
    }

    # Initialize validator
    validator = TemplateValidator()
    if not validator.fetch_available_nodes():
        print("❌ Could not validate nodes, aborting")
        return

    print("🔍 VALIDATING RELIABLE AI AGENT NODES")
    print("=" * 50)

    # Validate exactly what we need - most reliable approach
    required_nodes = [
        ("n8n-nodes-base.telegramTrigger", 1.2),
        ("n8n-nodes-base.code", 2),
        ("@n8n/n8n-nodes-langchain.agent", 1),
        ("@n8n/n8n-nodes-langchain.lmChatOllama", 1),
        ("n8n-nodes-base.telegram", 1.2)
    ]

    all_valid = True
    for node_type, version in required_nodes:
        is_valid, message = validator.validate_node(node_type, version)
        print(f"{'✅' if is_valid else '❌'} {node_type} v{version}: {message}")
        if not is_valid:
            all_valid = False

    if not all_valid:
        print("❌ Node validation failed")
        return

    print("\n✅ All nodes validated - deploying reliable AI agent...")

    # Reliable AI Agent with Local Mistral 7B
    reliable_ai_agent = {
        "name": f"🤖 Reliable AI Agent (Mistral 7B) - {datetime.now().strftime('%H:%M:%S')}",
        "nodes": [
            # 1. TELEGRAM TRIGGER
            {
                "parameters": {
                    "updates": ["message"]
                },
                "id": "telegram-trigger",
                "name": "Telegram Trigger",
                "type": "n8n-nodes-base.telegramTrigger",
                "typeVersion": 1.2,
                "position": [200, 300],
                "credentials": {"telegramApi": "Nn48haw1evoNGuWO"}
            },
            
            # 2. INPUT PROCESSOR
            {
                "parameters": {
                    "jsCode": '''
// Simple multimodal input processing
const message = $json.message || {};
let inputType = 'text';
let processedText = message.text || 'Hello AI!';
let context = '';

if (message.voice) {
    inputType = 'voice';
    context = `🎙️ Voice message (${message.voice.duration}s)`;
    processedText = `User sent a voice message. Please acknowledge this voice input and respond helpfully.`;
} else if (message.photo && message.photo.length > 0) {
    inputType = 'image';
    const photo = message.photo[message.photo.length - 1];
    context = `🖼️ Image ${photo.width}x${photo.height}`;
    processedText = `User sent an image. Please acknowledge this image and respond helpfully.`;
} else if (message.document) {
    inputType = 'document'; 
    context = `📄 ${message.document.file_name}`;
    processedText = `User sent a document named "${message.document.file_name}". Please acknowledge and help.`;
}

return [{
    json: {
        chat_id: message.chat.id,
        username: message.from.first_name || 'User',
        input_type: inputType,
        context: context,
        user_message: processedText
    }
}];
                    '''
                },
                "id": "input-processor",
                "name": "Input Processor",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [400, 300]
            },
            
            # 3. OLLAMA MISTRAL 7B (LangChain)
            {
                "parameters": {
                    "model": "mistral:7b",
                    "options": {
                        "baseURL": config["local_services"]["ollama"]
                    }
                },
                "id": "ollama-mistral",
                "name": "Ollama Mistral 7B",
                "type": "@n8n/n8n-nodes-langchain.lmChatOllama",
                "typeVersion": 1,
                "position": [600, 450]
            },
            
            # 4. AI AGENT (LangChain)
            {
                "parameters": {
                    "agent": "conversationalAgent",
                    "promptType": "define",
                    "text": "={{ $json.user_message }}",
                    "options": {
                        "systemMessage": "You are a helpful AI assistant for Telegram. You process different input types:\n\n🎙️ Voice messages - acknowledge audio input\n🖼️ Images - acknowledge visual content  \n📄 Documents - acknowledge files\n💬 Text - normal conversation\n\nBe friendly and helpful. Context: {{ $json.context }}\nUser: {{ $json.username }}",
                        "maxTokens": 500,
                        "temperature": 0.7
                    }
                },
                "id": "ai-agent",
                "name": "AI Agent",
                "type": "@n8n/n8n-nodes-langchain.agent",
                "typeVersion": 1,
                "position": [600, 300]
            },
            
            # 5. TELEGRAM RESPONSE
            {
                "parameters": {
                    "resource": "message",
                    "operation": "sendMessage", 
                    "chatId": "={{ $json.chat_id }}",
                    "text": "={{ $json.output }}",
                    "additionalFields": {
                        "disable_web_page_preview": True
                    }
                },
                "id": "telegram-send",
                "name": "Send Response",
                "type": "n8n-nodes-base.telegram",
                "typeVersion": 1.2,
                "position": [800, 300],
                "credentials": {"telegramApi": "Nn48haw1evoNGuWO"}
            }
        ],
        
        "connections": {
            "Telegram Trigger": {
                "main": [[{"node": "Input Processor", "type": "main", "index": 0}]]
            },
            "Input Processor": {
                "main": [[{"node": "AI Agent", "type": "main", "index": 0}]]
            },
            "AI Agent": {
                "main": [[{"node": "Send Response", "type": "main", "index": 0}]]
            },
            "Ollama Mistral 7B": {
                "ai_languageModel": [[{"node": "AI Agent", "type": "ai_languageModel", "index": 0}]]
            }
        },
        
        "settings": {}
    }

    print("\n🚀 DEPLOYING RELIABLE AI AGENT...")

    try:
        response = requests.post(
            f"{config['base_url']}/api/v1/workflows",
            headers=headers,
            json=reliable_ai_agent,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            workflow_info = response.json()
            workflow_id = workflow_info.get('id')
            print(f"\n✅ RELIABLE AI AGENT DEPLOYED!")
            print(f"🆔 Workflow ID: {workflow_id}")
            print(f"🌐 View in UI: {config['base_url']}/workflow/{workflow_id}")
            print(f"\n🎯 FEATURES:")
            print(f"✅ Telegram multimodal input (voice, image, document, text)")
            print(f"✅ Local Mistral 7B via LangChain Ollama")
            print(f"✅ AI Agent orchestration")
            print(f"✅ All nodes validated before deployment")
            print(f"\n🧪 READY FOR UI TESTING!")
            
        else:
            print(f"\n❌ Deployment failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()