#!/usr/bin/env python3

"""
Simple Generator - Telegram AI Workflow (Standard n8n nodes only)
Uses standard n8n nodes for multimodal processing with direct Ollama integration
Part of the Simple Generator system for non-LangChain workflows
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

# Use existing Telegram credential
TELEGRAM_CRED_ID = "Nn48haw1evoNGuWO"

# Simple Telegram AI workflow without LangChain
simple_telegram_workflow = {
    "name": f"🤖 Simple Telegram AI (No LangChain) - {datetime.now().strftime('%H:%M:%S')}",
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
        
        # 2. INPUT TYPE DETECTOR
        {
            "parameters": {
                "jsCode": '''
// Detect input type and process accordingly
const message = $json.message || {};

let inputType = 'text';
let processedText = message.text || 'No text content';
let metadata = {};

if (message.voice) {
    inputType = 'voice';
    processedText = `Voice message received (${message.voice.duration}s). File ID: ${message.voice.file_id}`;
    metadata = {
        duration: message.voice.duration,
        file_id: message.voice.file_id,
        mime_type: message.voice.mime_type
    };
} else if (message.photo && message.photo.length > 0) {
    inputType = 'image';
    const photo = message.photo[message.photo.length - 1];
    processedText = `Image received (${photo.width}x${photo.height}, ${Math.round(photo.file_size/1024)}KB)`;
    metadata = {
        width: photo.width,
        height: photo.height,
        file_size: photo.file_size,
        file_id: photo.file_id
    };
} else if (message.document) {
    inputType = 'document';
    processedText = `Document received: "${message.document.file_name}" (${Math.round(message.document.file_size/1024)}KB)`;
    metadata = {
        file_name: message.document.file_name,
        mime_type: message.document.mime_type,
        file_size: message.document.file_size,
        file_id: message.document.file_id
    };
}

return [{
    json: {
        chat_id: message.chat.id,
        user_id: message.from.id,
        username: message.from.username,
        input_type: inputType,
        processed_text: processedText,
        metadata: metadata,
        timestamp: new Date().toISOString()
    }
}];
                '''
            },
            "id": "input-detector",
            "name": "Input Type Detector",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [400, 400]
        },
        
        # 3. MEMORY STORAGE (Simple conversation context)
        {
            "parameters": {
                "jsCode": '''
// Simple memory management using workflow variables
const currentMessage = $json;
const chatId = currentMessage.chat_id;

// Get existing conversation from memory (you can enhance this with external storage)
const conversationKey = `conversation_${chatId}`;
let conversation = $vars[conversationKey] || [];

// Add current message to conversation
conversation.push({
    timestamp: currentMessage.timestamp,
    type: currentMessage.input_type,
    content: currentMessage.processed_text,
    metadata: currentMessage.metadata
});

// Keep only last 10 messages for context window
if (conversation.length > 10) {
    conversation = conversation.slice(-10);
}

// Store back in memory
$vars[conversationKey] = conversation;

// Build context for AI
const contextMessages = conversation.map(msg => 
    `[${msg.type}] ${msg.content}`
).join('\\n');

return [{
    json: {
        ...currentMessage,
        conversation_context: contextMessages,
        message_count: conversation.length
    }
}];
                '''
            },
            "id": "memory-manager",
            "name": "Simple Memory Manager", 
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [600, 400]
        },
        
        # 4. AI PROMPT BUILDER
        {
            "parameters": {
                "jsCode": '''
// Build comprehensive prompt for Ollama
const data = $json;

const systemPrompt = `You are a helpful AI assistant that can process multiple input types:
🎙️ Voice messages (transcribed)
🖼️ Images (metadata provided) 
📄 Documents (file information provided)
💬 Text messages

Current conversation context:
${data.conversation_context}

Latest message type: ${data.input_type}
Latest content: ${data.processed_text}

Respond appropriately based on the input type. Be helpful and acknowledge what type of content you received.`;

const ollamaPayload = {
    model: "mistral:7b",
    prompt: systemPrompt,
    stream: false,
    options: {
        temperature: 0.7,
        max_tokens: 1000
    }
};

return [{
    json: {
        ...data,
        ollama_payload: ollamaPayload,
        system_prompt: systemPrompt
    }
}];
                '''
            },
            "id": "prompt-builder",
            "name": "AI Prompt Builder",
            "type": "@n8n/n8n-nodes-base.code", 
            "typeVersion": 2,
            "position": [800, 400]
        },
        
        # 5. OLLAMA API CALL
        {
            "parameters": {
                "method": "POST",
                "url": f"{config['local_services']['ollama']}/api/generate",
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "model", "value": "={{ $json.ollama_payload.model }}"},
                        {"name": "prompt", "value": "={{ $json.ollama_payload.prompt }}"},
                        {"name": "stream", "value": "={{ $json.ollama_payload.stream }}"},
                        {"name": "options", "value": "={{ $json.ollama_payload.options }}"}
                    ]
                },
                "options": {
                    "bodyContentType": "json",
                    "timeout": 30000
                }
            },
            "id": "ollama-request",
            "name": "Ollama API Call",
            "type": "@n8n/n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [1000, 400]
        },
        
        # 6. RESPONSE FORMATTER
        {
            "parameters": {
                "jsCode": '''
// Format AI response for Telegram
const inputData = $input.first().json;
const ollamaResponse = $json;

let aiResponse = "I encountered an issue processing your request.";

if (ollamaResponse.response) {
    aiResponse = ollamaResponse.response;
} else if (ollamaResponse.message) {
    aiResponse = `Error: ${ollamaResponse.message}`;
}

// Add input type acknowledgment
const typeEmojis = {
    'voice': '🎙️',
    'image': '🖼️', 
    'document': '📄',
    'text': '💬'
};

const typeEmoji = typeEmojis[inputData.input_type] || '💬';
const finalResponse = `${typeEmoji} ${aiResponse}`;

return [{
    json: {
        chat_id: inputData.chat_id,
        response_text: finalResponse,
        input_type: inputData.input_type,
        processing_time: new Date().toISOString()
    }
}];
                '''
            },
            "id": "response-formatter",
            "name": "Response Formatter",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1200, 400]
        },
        
        # 7. TELEGRAM RESPONSE
        {
            "parameters": {
                "resource": "message",
                "operation": "sendMessage",
                "chatId": "={{ $json.chat_id }}",
                "text": "={{ $json.response_text }}",
                "additionalFields": {
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                }
            },
            "id": "telegram-send",
            "name": "Send Telegram Response",
            "type": "@n8n/n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [1400, 400],
            "credentials": {"telegramApi": TELEGRAM_CRED_ID}
        }
    ],
    
    "connections": {
        "Telegram Trigger": {
            "main": [[{"node": "Input Type Detector", "type": "main", "index": 0}]]
        },
        "Input Type Detector": {
            "main": [[{"node": "Simple Memory Manager", "type": "main", "index": 0}]]
        },
        "Simple Memory Manager": {
            "main": [[{"node": "AI Prompt Builder", "type": "main", "index": 0}]]
        },
        "AI Prompt Builder": {
            "main": [[{"node": "Ollama API Call", "type": "main", "index": 0}]]
        },
        "Ollama API Call": {
            "main": [[{"node": "Response Formatter", "type": "main", "index": 0}]]
        },
        "Response Formatter": {
            "main": [[{"node": "Send Telegram Response", "type": "main", "index": 0}]]
        }
    },
    "settings": {}
}

print("🔍 SIMPLE TELEGRAM AI WORKFLOW (No LangChain)")
print("=" * 60)
print()

print("📋 FEATURES SUPPORTED:")
print("✅ Multimodal input detection (voice, image, document, text)")
print("✅ Simple conversation memory (last 10 messages)")
print("✅ Direct Ollama integration (mistral:7b)")
print("✅ Response formatting with input type acknowledgment")
print("✅ Works with standard n8n nodes only")
print()

print("❌ LIMITATIONS vs LangChain Version:")
print("• No unified AI agent orchestration")
print("• Manual memory management in variables") 
print("• No built-in tool integration (calculator, web search)")
print("• No context engineering automation")
print("• No conversation flow optimization")
print()

print("🔧 NODES USED:")
print("• Telegram Trigger & Send nodes")
print("• Code nodes for processing logic")
print("• HTTP Request for Ollama API") 
print("• Standard workflow variables for memory")
print()

print(f"🚀 Deploying simple Telegram AI workflow...")

try:
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=simple_telegram_workflow,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        workflow_info = response.json()
        workflow_id = workflow_info.get('id')
        print(f"✅ SIMPLE TELEGRAM AI DEPLOYED!")
        print(f"🆔 Workflow ID: {workflow_id}")
        print(f"🌐 View: {config['base_url']}/workflow/{workflow_id}")
        print()
        
        print("🧪 TESTING SCENARIOS:")
        print("1. 🎙️ Send voice message → Should detect and acknowledge voice")
        print("2. 🖼️ Send image → Should detect image metadata")
        print("3. 📄 Send document → Should detect file information")
        print("4. 💬 Send text → Should respond with AI conversation")
        print("5. 🧠 Multiple messages → Should maintain conversation context")
        
    else:
        print(f"❌ Deployment failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")