#!/usr/bin/env python3

"""
Test Basic Workflow - Verify n8n nodes are working
Simple workflow to test node compatibility
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

# Basic test workflow with minimal nodes
basic_test_workflow = {
    "name": f"🧪 Basic Node Test - {datetime.now().strftime('%H:%M:%S')}",
    "nodes": [
        # 1. MANUAL TRIGGER (always works)
        {
            "parameters": {},
            "id": "manual-trigger",
            "name": "Manual Trigger",
            "type": "@n8n/n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [200, 300]
        },
        
        # 2. SET NODE (basic data processing)
        {
            "parameters": {
                "values": {
                    "string": [
                        {
                            "name": "test_message",
                            "value": "Hello from n8n test workflow!"
                        },
                        {
                            "name": "timestamp",
                            "value": "={{ new Date().toISOString() }}"
                        }
                    ]
                }
            },
            "id": "set-data",
            "name": "Set Test Data",
            "type": "@n8n/n8n-nodes-base.set",
            "typeVersion": 3.3,
            "position": [400, 300]
        },
        
        # 3. CODE NODE (test JavaScript execution)
        {
            "parameters": {
                "jsCode": '''
// Test JavaScript execution in n8n
const inputData = $json;
console.log('Input data:', inputData);

const result = {
    original_message: inputData.test_message,
    processed_at: inputData.timestamp,
    node_test_result: "✅ Code node working",
    javascript_features: {
        variables: "working",
        functions: "working",
        json_processing: "working"
    },
    test_calculations: {
        simple_math: 2 + 2,
        string_length: inputData.test_message.length,
        current_time: new Date().toISOString()
    }
};

return [{json: result}];
                '''
            },
            "id": "code-test",
            "name": "Code Node Test",
            "type": "@n8n/n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [600, 300]
        },
        
        # 4. HTTP REQUEST (test external connectivity)
        {
            "parameters": {
                "method": "GET",
                "url": "https://httpbin.org/json",
                "options": {
                    "timeout": 10000
                }
            },
            "id": "http-test",
            "name": "HTTP Request Test",
            "type": "@n8n/n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [800, 300]
        },
        
        # 5. MERGE NODE (test data combination)
        {
            "parameters": {
                "mode": "mergeByPosition"
            },
            "id": "merge-results",
            "name": "Merge Test Results",
            "type": "@n8n/n8n-nodes-base.merge",
            "typeVersion": 2.1,
            "position": [1000, 300]
        }
    ],
    
    "connections": {
        "Manual Trigger": {
            "main": [[{"node": "Set Test Data", "type": "main", "index": 0}]]
        },
        "Set Test Data": {
            "main": [[{"node": "Code Node Test", "type": "main", "index": 0}]]
        },
        "Code Node Test": {
            "main": [[{"node": "Merge Test Results", "type": "main", "index": 0}]]
        },
        "HTTP Request Test": {
            "main": [[{"node": "Merge Test Results", "type": "main", "index": 1}]]
        }
    },
    "settings": {}
}

print("🧪 BASIC NODE COMPATIBILITY TEST")
print("=" * 50)
print()

print("🔧 NODES TO TEST:")
print("✓ Manual Trigger - Always available trigger")
print("✓ Set Node - Basic data processing")
print("✓ Code Node - JavaScript execution")
print("✓ HTTP Request - External connectivity")
print("✓ Merge Node - Data combination")
print()

print("🚀 Deploying basic test workflow...")

try:
    response = requests.post(
        f"{config['base_url']}/api/v1/workflows",
        headers=headers,
        json=basic_test_workflow,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        workflow_info = response.json()
        workflow_id = workflow_info.get('id')
        print(f"✅ BASIC TEST WORKFLOW DEPLOYED!")
        print(f"🆔 Workflow ID: {workflow_id}")
        print(f"🌐 View: {config['base_url']}/workflow/{workflow_id}")
        print()
        
        # Try to execute the workflow for testing
        print("🧪 EXECUTING TEST WORKFLOW...")
        exec_response = requests.post(
            f"{config['base_url']}/api/v1/workflows/{workflow_id}/execute",
            headers=headers,
            json={},
            timeout=30
        )
        
        if exec_response.status_code in [200, 201]:
            exec_result = exec_response.json()
            print(f"✅ EXECUTION SUCCESSFUL!")
            print(f"📊 Execution ID: {exec_result.get('id', 'unknown')}")
            
            # Check execution results after a moment
            import time
            time.sleep(3)
            
            result_response = requests.get(
                f"{config['base_url']}/api/v1/executions/{exec_result.get('id')}",
                headers=headers,
                timeout=10
            )
            
            if result_response.status_code == 200:
                result_data = result_response.json()
                print(f"🎯 EXECUTION STATUS: {result_data.get('status', 'unknown')}")
                if result_data.get('status') == 'success':
                    print("🎉 ALL NODES WORKING CORRECTLY!")
                else:
                    print("⚠️ Some nodes may have issues")
            
        else:
            print(f"⚠️ Execution failed: {exec_response.status_code}")
            print(f"Response: {exec_response.text}")
        
    else:
        print(f"❌ Deployment failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")