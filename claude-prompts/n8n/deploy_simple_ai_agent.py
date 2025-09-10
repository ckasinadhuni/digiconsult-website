#!/usr/bin/env python3

"""
Simple AI Agent with Multimodal Telegram Input - VALIDATED
Uses proper node validation and LangChain integration
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

    print("🔍 PRE-DEPLOYMENT VALIDATION")
    print("=" * 50)

    # Validate required nodes
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
        print("❌ Node validation failed, cannot proceed")
        return

    print("\n✅ All nodes validated, proceeding with deployment...")

    # Simple AI Agent with Multimodal Telegram
    simple_ai_agent = {
        "name": f"🤖 Simple AI Agent - {datetime.now().strftime('%H:%M:%S')}",
        "nodes": [
            # 1. TELEGRAM TRIGGER - Validated
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
            
            # 2. INPUT PROCESSOR - Validated
            {
                "parameters": {
                    "jsCode": '''
// Process multimodal input types
const message = $json.message || {};
let inputType = 'text';
let processedText = message.text || 'No text content';
let inputInfo = '';

if (message.voice) {
    inputType = 'voice';
    inputInfo = `🎙️ Voice message (${message.voice.duration}s)`;
    processedText = `User sent a voice message lasting ${message.voice.duration} seconds. Please acknowledge the voice input and respond helpfully.`;
} else if (message.photo && message.photo.length > 0) {
    inputType = 'photo';
    const photo = message.photo[message.photo.length - 1];
    inputInfo = `🖼️ Image (${photo.width}x${photo.height})`;
    processedText = `User sent an image that is ${photo.width}x${photo.height} pixels. Please acknowledge the image and respond helpfully.`;
} else if (message.document) {
    inputType = 'document';
    inputInfo = `📄 Document: ${message.document.file_name}`;
    processedText = `User sent a document named "${message.document.file_name}". Please acknowledge the document and respond helpfully.`;
} else if (message.text) {
    inputType = 'text';
    inputInfo = `💬 Text message`;
    processedText = message.text;
}

return [{
    json: {
        chat_id: message.chat.id,
        user_id: message.from.id,
        username: message.from.username || message.from.first_name,
        input_type: inputType,
        input_info: inputInfo,
        processed_text: processedText,
        original_message: message
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
            
            # 3. AI AGENT - Validated LangChain
            {
                "parameters": {
                    "agent": "conversationalAgent",
                    "promptType": "define",
                    "text": "={{ $json.processed_text }}",
                    "options": {
                        "systemMessage": "You are a helpful AI assistant integrated with Telegram. You can process different types of input:\n\n🎙️ Voice messages - I acknowledge audio input\n🖼️ Images - I can see image metadata and respond contextually\n📄 Documents - I can help with document-related questions\n💬 Text - Natural conversation\n\nAlways acknowledge the input type received and provide helpful responses. Be friendly and conversational. Current input type: {{ $json.input_type }}\nInput details: {{ $json.input_info }}",
                        "maxTokens": 1000,
                        "temperature": 0.7
                    }
                },
                "id": "ai-agent",
                "name": "AI Agent",
                "type": "@n8n/n8n-nodes-langchain.agent",
                "typeVersion": 1,
                "position": [600, 300]
            },
            
            # 4. OLLAMA CHAT MODEL - Validated LangChain
            {
                "parameters": {
                    "model": "mistral:7b",
                    "options": {
                        "baseURL": config["local_services"]["ollama"],
                        "temperature": 0.7,
                        "maxTokens": 800
                    }
                },
                "id": "ollama-chat",
                "name": "Ollama Mistral 7B",
                "type": "@n8n/n8n-nodes-langchain.lmChatOllama",
                "typeVersion": 1,
                "position": [600, 480]
            },
            
            # 5. TELEGRAM RESPONSE - Validated
            {
                "parameters": {
                    "resource": "message",
                    "operation": "sendMessage",
                    "chatId": "={{ $json.chat_id }}",
                    "text": "={{ $json.output }}",
                    "additionalFields": {
                        "parse_mode": "Markdown",
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

    print("\n🚀 DEPLOYING SIMPLE AI AGENT...")

    try:
        response = requests.post(
            f"{config['base_url']}/api/v1/workflows",
            headers=headers,
            json=simple_ai_agent,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            workflow_info = response.json()
            workflow_id = workflow_info.get('id')
            print(f"\n✅ SIMPLE AI AGENT DEPLOYED!")
            print(f"🆔 Workflow ID: {workflow_id}")
            print(f"🌐 View: {config['base_url']}/workflow/{workflow_id}")
            print(f"\n📱 FEATURES:")
            print(f"✅ Telegram trigger with multimodal input detection")
            print(f"✅ Voice, image, document, text processing")
            print(f"✅ LangChain AI Agent with Ollama Mistral 7B")
            print(f"✅ Contextual responses based on input type")
            print(f"\n🧪 TEST IN UI:")
            print(f"1. Go to: {config['base_url']}/workflow/{workflow_id}")
            print(f"2. Activate the workflow")
            print(f"3. Send messages to your Telegram bot")
            print(f"4. Test voice, images, documents, and text")
            
        else:
            print(f"\n❌ Deployment failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()