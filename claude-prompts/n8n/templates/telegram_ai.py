#!/usr/bin/env python3

"""
Telegram AI Assistant Template Generator
Optimized for current n8n LangChain best practices
"""

def generate_telegram_ai_template(credentials, local_services, **kwargs):
    """Generate modern Telegram AI workflow with current best practices"""
    
    telegram_cred = credentials.get('telegramApi', [{}])[0].get('id', 'MISSING_TELEGRAM_CREDS')
    
    template = {
        "trigger_nodes": [
            {
                "type": "@n8n/n8n-nodes-base.telegramTrigger",
                "parameters": {"updates": ["message"]},
                "credentials": {"telegramApi": telegram_cred}
            }
        ],
        "processing_nodes": [
            {
                "type": "@n8n/n8n-nodes-base.switch",
                "purpose": "route_message_types",
                "conditions": ["voice", "photo", "document", "text"]
            },
            {
                "type": "@n8n/n8n-nodes-base.httpRequest", 
                "purpose": "transcribe_voice",
                "url": f"{local_services['whisper']}/transcribe"
            },
            {
                "type": "@n8n/n8n-nodes-langchain.agent",
                "purpose": "ai_processing",
                "agent_type": "conversationalAgent"
            },
            {
                "type": "@n8n/n8n-nodes-langchain.chatOllama",
                "purpose": "language_model",
                "model": "mistral:7b",
                "baseURL": local_services['ollama']
            }
        ],
        "output_nodes": [
            {
                "type": "@n8n/n8n-nodes-base.telegram",
                "operation": "sendMessage",
                "credentials": {"telegramApi": telegram_cred}
            }
        ],
        "features": {
            "voice_transcription": True,
            "image_analysis": True,
            "action_buttons": True,
            "context_awareness": True
        }
    }
    
    return template