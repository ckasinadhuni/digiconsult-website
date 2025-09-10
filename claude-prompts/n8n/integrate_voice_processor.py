#!/usr/bin/env python3

"""
Integrate voice processing into unified Enhanced Input Processor
"""

import json
import requests

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    headers = {'X-N8N-API-KEY': config['api_key']}
    template_id = 'kaVhNfbnkr3tw0j2'

    print('🔧 INTEGRATING VOICE INTO UNIFIED INPUT PROCESSOR')
    print('=' * 55)

    response = requests.get(f"{config['base_url']}/api/v1/workflows/{template_id}", headers=headers)
    workflow = response.json()

    # Update Enhanced Input Processor to handle ALL inputs
    for node in workflow['nodes']:
        if node['name'] == 'Enhanced Input Processor':
            node['parameters']['jsCode'] = '''// Check if this is transcribed voice data
const isVoiceTranscription = $input.itemMatching(0) && $input.itemMatching(0).json.text;
let message, transcription;

if (isVoiceTranscription) {
    // Voice transcription flow - multiple inputs
    transcription = $input.itemMatching(0).json;
    message = $input.itemMatching(1).json.message || {};
} else {
    // Direct message flow (text, photo, document, etc.)
    message = $json.message || {};
    transcription = null;
}

let inputType = 'text';
let processedText = message.text || 'Hello AI!';
let context = '';
let command = null;
let searchQuery = '';

// Handle transcribed voice input
if (transcription && transcription.text) {
    inputType = 'voice';
    context = '🎙️ Voice transcribed: ' + (message.voice ? message.voice.duration + 's' : '');
    processedText = transcription.text;
    
    // Check if transcribed text contains commands
    if (transcription.text.toLowerCase().startsWith('search ')) {
        command = 'vector_search';
        searchQuery = transcription.text.substring(7);
        context += ' (search command detected)';
    }
}
// Handle direct text input
else if (message.text) {
    if (message.text.startsWith('/search ')) {
        command = 'vector_search';
        searchQuery = message.text.substring(8);
        processedText = searchQuery;
        context = '🔍 Vector search command';
    } else if (message.text.startsWith('/files ')) {
        command = 'file_search';
        searchQuery = message.text.substring(7);
        processedText = searchQuery;
        context = '📁 File search command';
    }
}
// Handle other multimodal inputs
else if (message.photo && message.photo.length > 0) {
    inputType = 'image';
    context = '🖼️ Image received';
    processedText = 'User sent an image. Please analyze and respond.';
} else if (message.document) {
    inputType = 'document';
    context = '📄 Document received';
    processedText = 'User sent a document. Please process and respond.';
}

return [{
    json: {
        chat_id: message.chat.id,
        username: message.from.first_name || 'User',
        input_type: inputType,
        context: context,
        user_message: processedText,
        command: command,
        search_query: searchQuery,
        original_duration: message.voice ? message.voice.duration : null
    }
}];'''
            print('✅ Enhanced Input Processor updated to handle voice transcription')
            break

    # Update connections - route voice transcription to unified processor
    workflow['connections']['Transcribe Voice'] = {
        'main': [
            [{'node': 'Enhanced Input Processor', 'type': 'main', 'index': 0}]
        ]
    }

    # Remove the redundant Voice Input Processor node
    workflow['nodes'] = [node for node in workflow['nodes'] if node['name'] != 'Voice Input Processor']
    print('✅ Removed redundant Voice Input Processor node')

    # Clean up connections
    if 'Voice Input Processor' in workflow['connections']:
        del workflow['connections']['Voice Input Processor']

    print('✅ Updated transcription flow to use unified processor')

    workflow_update = {
        'name': workflow['name'],
        'nodes': workflow['nodes'],
        'connections': workflow['connections'],
        'settings': workflow.get('settings', {})
    }

    response = requests.put(
        f"{config['base_url']}/api/v1/workflows/{template_id}",
        headers=headers,
        json=workflow_update
    )

    print(f'\nUpdate Status: {response.status_code}')
    if response.status_code == 200:
        print('✅ UNIFIED INPUT PROCESSOR COMPLETE!')
        print('\n📱 Voice: Switch → Get File → Transcribe → Enhanced Input Processor → AI Agent')
        print('💬 Text: Switch → Enhanced Input Processor → AI Agent')  
        print('🖼️ All inputs now use single processor seamlessly')
    else:
        print(f'❌ Error: {response.text}')

if __name__ == "__main__":
    main()