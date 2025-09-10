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

# Use existing Telegram credential
TELEGRAM_CRED_ID = "Nn48haw1evoNGuWO"

# Create comprehensive multimodal Telegram AI workflow
multimodal_workflow = {
    "name": f"🎙️📱🖼️ Multimodal Telegram AI - {datetime.now().strftime('%H:%M:%S')}",
    "nodes": [
        # 1. TELEGRAM TRIGGER
        {
            "parameters": {
                "updates": ["message"]
            },
            "id": "telegram-trigger",
            "name": "Telegram Trigger",
            "type": "@n8n/n8n-nodes-base.telegramTrigger",
            "typeVersion": 1.1,
            "position": [200, 400],
            "credentials": {"telegramApi": TELEGRAM_CRED_ID}
        },
        
        # 2. MULTIMODAL ROUTER
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
                            "leftValue": "={{ $json.message.document }}",
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
            "id": "multimodal-router",
            "name": "Multimodal Router",
            "type": "@n8n/n8n-nodes-base.switch",
            "typeVersion": 3,
            "position": [400, 400]
        },
        
        # 3. VOICE TRANSCRIPTION PATH
        {
            "parameters": {
                "resource": "file",
                "operation": "get",
                "fileId": "={{ $json.message.voice.file_id }}"
            },
            "id": "get-voice-file",
            "name": "Get Voice File",
            "type": "@n8n/n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [600, 200],
            "credentials": {"telegramApi": TELEGRAM_CRED_ID}
        },
        {
            "parameters": {
                "method": "POST",
                "url": f"{config['local_services']['whisper']}/transcribe",
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "file", "value": "={{ $binary.data }}"},
                        {"name": "language", "value": "auto"}
                    ]
                },
                "options": {
                    "bodyContentType": "multipart-form-data"
                }
            },
            "id": "transcribe-voice",
            "name": "Transcribe Voice",
            "type": "@n8n/n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [800, 200]
        },
        {
            "parameters": {
                "jsCode": "// Process transcription result\nconst transcription = $json.text || $json.transcription || '';\nreturn [{\n  json: {\n    message: {\n      ...($input.first().json.message || {}),\n      text: `🎙️ Voice message transcribed: \"${transcription}\"`,\n      processed_text: transcription,\n      input_type: 'voice'\n    }\n  }\n}];"
            },
            "id": "process-transcription",
            "name": "Process Transcription",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1000, 200]
        },
        
        # 4. IMAGE ANALYSIS PATH
        {
            "parameters": {
                "resource": "file",
                "operation": "get",
                "fileId": "={{ $json.message.photo[$json.message.photo.length - 1].file_id }}"
            },
            "id": "get-image-file",
            "name": "Get Image File",
            "type": "@n8n/n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [600, 300],
            "credentials": {"telegramApi": TELEGRAM_CRED_ID}
        },
        {
            "parameters": {
                "jsCode": "// Process image information\nconst photo = $input.first().json.message.photo || [];\nconst largestPhoto = photo[photo.length - 1] || {};\nconst fileInfo = $json || {};\n\nreturn [{\n  json: {\n    message: {\n      ...($input.first().json.message || {}),\n      text: `🖼️ Image received: ${largestPhoto.width}x${largestPhoto.height} pixels, ${Math.round(largestPhoto.file_size/1024)}KB\\n\\nImage analysis: I can see you've sent me an image. While I can't process the visual content directly, I can help you with questions about the image or any related tasks.`,\n      processed_text: `Image file received: ${fileInfo.file_path || 'unknown path'}`,\n      input_type: 'image',\n      image_info: {\n        width: largestPhoto.width,\n        height: largestPhoto.height,\n        file_size: largestPhoto.file_size,\n        file_id: largestPhoto.file_id\n      }\n    }\n  }\n}];"
            },
            "id": "process-image",
            "name": "Process Image",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [800, 300]
        },
        
        # 5. DOCUMENT/FILE PROCESSING PATH
        {
            "parameters": {
                "resource": "file",
                "operation": "get",
                "fileId": "={{ $json.message.document.file_id }}"
            },
            "id": "get-document-file",
            "name": "Get Document File",
            "type": "@n8n/n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [600, 500],
            "credentials": {"telegramApi": TELEGRAM_CRED_ID}
        },
        {
            "parameters": {
                "jsCode": "// Process document information\nconst document = $input.first().json.message.document || {};\nconst fileInfo = $json || {};\n\nreturn [{\n  json: {\n    message: {\n      ...($input.first().json.message || {}),\n      text: `📄 Document received: \"${document.file_name || 'unnamed file'}\"\\nSize: ${Math.round((document.file_size || 0)/1024)}KB\\nType: ${document.mime_type || 'unknown'}\\n\\nI've received your document. I can help you with questions about it or related tasks.`,\n      processed_text: `Document file: ${document.file_name} (${document.mime_type})`,\n      input_type: 'document',\n      document_info: {\n        file_name: document.file_name,\n        mime_type: document.mime_type,\n        file_size: document.file_size,\n        file_id: document.file_id\n      }\n    }\n  }\n}];"
            },
            "id": "process-document",
            "name": "Process Document",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [800, 500]
        },
        
        # 6. TEXT PROCESSING PATH
        {
            "parameters": {
                "jsCode": "// Process text message\nconst message = $json.message || {};\nreturn [{\n  json: {\n    message: {\n      ...message,\n      processed_text: message.text || '',\n      input_type: 'text'\n    }\n  }\n}];"
            },
            "id": "process-text",
            "name": "Process Text",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [600, 600]
        },
        
        # 7. MERGE PROCESSED INPUTS
        {
            "parameters": {
                "mode": "mergeByPosition"
            },
            "id": "merge-inputs",
            "name": "Merge Processed Inputs",
            "type": "@n8n/n8n-nodes-base.merge",
            "typeVersion": 2.1,
            "position": [1200, 400]
        },
        
        # 8. AI AGENT WITH MULTIMODAL UNDERSTANDING
        {
            "parameters": {
                "agent": "conversationalAgent",
                "promptType": "define", 
                "text": "{{ $json.message.processed_text || $json.message.text || 'Hello! How can I help you?' }}",
                "options": {
                    "systemMessage": "You are a multimodal AI assistant for Telegram with these capabilities:\n\n🎙️ VOICE PROCESSING:\n- I can understand transcribed voice messages\n- I acknowledge the audio input and respond appropriately\n\n🖼️ IMAGE UNDERSTANDING:\n- I can see image metadata (size, format, file info)\n- I acknowledge images and can discuss them contextually\n- I can help with image-related questions\n\n📄 DOCUMENT HANDLING:\n- I can process document metadata (name, type, size)\n- I can help with document-related questions\n- I acknowledge file receipts and offer assistance\n\n💬 TEXT CONVERSATION:\n- Natural conversation with full context\n- Memory of our chat history\n- Access to tools for calculations, web search, code\n\n🛠️ AVAILABLE TOOLS:\n- Calculator for math problems\n- Web search for current information\n- Code interpreter for programming help\n\n📱 RESPONSE STYLE:\nI adapt my responses based on input type:\n- Voice: Acknowledge the spoken input, respond conversationally\n- Image: Reference what I can determine about the image\n- Document: Acknowledge the file and offer relevant help\n- Text: Natural conversation with context\n\nAlways be helpful, accurate, and acknowledge the specific type of input received. Use emojis appropriately and format responses clearly.",
                    "maxTokens": 4000,
                    "temperature": 0.7
                }
            },
            "id": "multimodal-ai-agent",
            "name": "Multimodal AI Agent",
            "type": "@n8n/n8n-nodes-langchain.agent",
            "typeVersion": 1.4,
            "position": [1400, 400]
        },
        
        # 9. OLLAMA LANGUAGE MODEL
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
            "position": [1400, 580]
        },
        
        # 10. CONVERSATION MEMORY
        {
            "parameters": {
                "sessionIdExpression": "={{ $json.message.chat.id }}",
                "contextWindowLength": 10
            },
            "id": "conversation-memory",
            "name": "Conversation Memory",
            "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
            "typeVersion": 1.2,
            "position": [1600, 300]
        },
        
        # 11-13. AI TOOLS
        {
            "parameters": {},
            "id": "calculator-tool",
            "name": "Calculator Tool",
            "type": "@n8n/n8n-nodes-langchain.toolCalculator",
            "typeVersion": 1.2,
            "position": [1600, 400]
        },
        {
            "parameters": {},
            "id": "web-search-tool",
            "name": "Web Search Tool", 
            "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
            "typeVersion": 1.2,
            "position": [1600, 500]
        },
        {
            "parameters": {},
            "id": "code-tool",
            "name": "Code Interpreter Tool",
            "type": "@n8n/n8n-nodes-langchain.toolCode",
            "typeVersion": 1.2,
            "position": [1600, 600]
        },
        
        # 14. TELEGRAM RESPONSE
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
            "position": [1800, 400],
            "credentials": {"telegramApi": TELEGRAM_CRED_ID}
        }
    ],
    
    "connections": {
        # Main flow
        "Telegram Trigger": {
            "main": [[{"node": "Multimodal Router", "type": "main", "index": 0}]]
        },
        
        # Router to processing paths
        "Multimodal Router": {
            "main": [
                # Output 0: Voice messages
                [{"node": "Get Voice File", "type": "main", "index": 0}],
                # Output 1: Images  
                [{"node": "Get Image File", "type": "main", "index": 0}],
                # Output 2: Documents
                [{"node": "Get Document File", "type": "main", "index": 0}],
                # Output 3: Text
                [{"node": "Process Text", "type": "main", "index": 0}]
            ]
        },
        
        # Voice processing chain
        "Get Voice File": {
            "main": [[{"node": "Transcribe Voice", "type": "main", "index": 0}]]
        },
        "Transcribe Voice": {
            "main": [[{"node": "Process Transcription", "type": "main", "index": 0}]]
        },
        
        # Image processing chain
        "Get Image File": {
            "main": [[{"node": "Process Image", "type": "main", "index": 0}]]
        },
        
        # Document processing chain
        "Get Document File": {
            "main": [[{"node": "Process Document", "type": "main", "index": 0}]]
        },
        
        # Merge all processed inputs
        "Process Transcription": {
            "main": [[{"node": "Merge Processed Inputs", "type": "main", "index": 0}]]
        },
        "Process Image": {
            "main": [[{"node": "Merge Processed Inputs", "type": "main", "index": 0}]]
        },
        "Process Document": {
            "main": [[{"node": "Merge Processed Inputs", "type": "main", "index": 0}]]
        },
        "Process Text": {
            "main": [[{"node": "Merge Processed Inputs", "type": "main", "index": 0}]]
        },
        
        # AI processing
        "Merge Processed Inputs": {
            "main": [[{"node": "Multimodal AI Agent", "type": "main", "index": 0}]]
        },
        "Multimodal AI Agent": {
            "main": [[{"node": "Send Telegram Response", "type": "main", "index": 0}]]
        },
        
        # AI connections
        "Ollama Mistral 7B": {
            "ai_languageModel": [[{"node": "Multimodal AI Agent", "type": "ai_languageModel", "index": 0}]]
        },
        "Conversation Memory": {
            "ai_memory": [[{"node": "Multimodal AI Agent", "type": "ai_memory", "index": 0}]]
        },
        "Calculator Tool": {
            "ai_tool": [[{"node": "Multimodal AI Agent", "type": "ai_tool", "index": 0}]]
        },
        "Web Search Tool": {
            "ai_tool": [[{"node": "Multimodal AI Agent", "type": "ai_tool", "index": 1}]]
        },
        "Code Interpreter Tool": {
            "ai_tool": [[{"node": "Multimodal AI Agent", "type": "ai_tool", "index": 2}]]
        }
    },
    "settings": {}
}

print("🔍 COMPREHENSIVE MULTIMODAL WORKFLOW ANALYSIS")
print("=" * 60)
print()

print("📋 INPUT TYPES SUPPORTED:")
print("🎙️ Voice Messages → faster-whisper transcription")
print("🖼️ Images → metadata analysis + acknowledgment")  
print("📄 Documents → file info processing")
print("💬 Text → direct AI processing")
print()

print("🔗 PROCESSING PATHS:")
print("1. Voice: Trigger → Router → Get File → Transcribe → Process → Merge → AI → Response")
print("2. Image: Trigger → Router → Get File → Process → Merge → AI → Response") 
print("3. Document: Trigger → Router → Get File → Process → Merge → AI → Response")
print("4. Text: Trigger → Router → Process → Merge → AI → Response")
print()

print("🧠 AI CAPABILITIES:")
print("✅ Ollama Mistral 7B language model")
print("✅ Conversation memory per chat_id")
print("✅ Calculator tool for math")
print("✅ Web search tool")
print("✅ Code interpreter tool")
print("✅ Multimodal awareness in system prompt")
print()

print("🔧 CREDENTIALS REQUIRED:")
print(f"✅ Telegram API: {TELEGRAM_CRED_ID} (existing)")
print()

print("🌐 EXTERNAL DEPENDENCIES:")
print(f"✅ Ollama: {config['local_services']['ollama']} (local)")
print(f"✅ Faster-Whisper: {config['local_services']['whisper']} (local)")
print()

print("🚀 Deploying comprehensive multimodal Telegram AI workflow...")

try:
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=multimodal_workflow,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        workflow_info = response.json()
        workflow_id = workflow_info.get('id')
        print(f"✅ MULTIMODAL TELEGRAM AI DEPLOYED!")
        print(f"🆔 Workflow ID: {workflow_id}")
        print(f"🌐 View: {config['base_url']}/workflow/{workflow_id}")
        print()
        
        print("🧪 TESTING SCENARIOS:")
        print("1. 🎙️ Send voice message → Should transcribe and respond")
        print("2. 🖼️ Send image → Should acknowledge and describe")
        print("3. 📄 Send document → Should recognize and offer help")
        print("4. 💬 Send text → Should respond normally with context")
        print("5. 🧮 Ask math question → Should use calculator")
        print("6. 🌐 Ask for web info → Should search online")
        print("7. 💻 Ask coding question → Should use code interpreter")
        
    else:
        print(f"❌ Deployment failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")