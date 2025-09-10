#!/usr/bin/env python3

"""
Reliable n8n API Helper - Tested endpoint calls
"""

import json
import requests

class N8nAPI:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.base_url = config['base_url']
        self.headers = {
            'X-N8N-API-KEY': config['api_key'],
            'Content-Type': 'application/json'
        }

    def get_workflow(self, workflow_id):
        """Get workflow - tested working endpoint"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                return True, result.get('data', result)
            else:
                return False, f"Status {response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)

    def update_workflow(self, workflow_id, workflow_data):
        """Update workflow - tested working endpoint"""
        try:
            response = requests.put(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                json=workflow_data,
                timeout=30
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"Status {response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)

    def get_workflow_executions(self, workflow_id, limit=5):
        """Get workflow execution history"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/executions",
                headers=self.headers,
                params={'filter': json.dumps({'workflowId': workflow_id}), 'limit': limit},
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()['data']
            else:
                return False, f"Status {response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)

def main():
    api = N8nAPI()
    
    print("🔧 FIXING ENHANCED AI AGENT ROUTER")
    print("=" * 50)
    
    workflow_id = 'jyskZP1sldP7NwYA'
    
    # Get current workflow
    success, workflow = api.get_workflow(workflow_id)
    if not success:
        print(f"❌ Failed to get workflow: {workflow}")
        return
    
    print(f"✅ Got workflow: {workflow['name']}")
    print(f"📊 Current nodes: {len(workflow['nodes'])}")
    
    # Find and fix the router node
    router_node = None
    for node in workflow['nodes']:
        if node['type'] == 'n8n-nodes-base.switch' and 'router' in node['name'].lower():
            router_node = node
            break
    
    if not router_node:
        print("❌ No router node found")
        return
    
    print(f"🔍 Found router: {router_node['name']}")
    
    # Current conditions
    current_conditions = router_node['parameters'].get('conditions', {}).get('conditions', [])
    print(f"📋 Current conditions: {len(current_conditions)}")
    for i, cond in enumerate(current_conditions):
        print(f"  {i}: {cond.get('leftValue', '?')} {cond.get('operator', {}).get('operation', '?')}")
    
    # Fix router with proper multimodal conditions
    fixed_conditions = {
        "options": {"caseSensitive": False, "leftValue": "", "typeValidation": "strict"},
        "conditions": [
            # Command routing
            {
                "id": "search_cmd",
                "leftValue": "={{ $json.message.text }}",
                "operator": {"type": "string", "operation": "startsWith", "rightValue": "/search"}
            },
            {
                "id": "files_cmd", 
                "leftValue": "={{ $json.message.text }}",
                "operator": {"type": "string", "operation": "startsWith", "rightValue": "/files"}
            },
            # Multimodal routing
            {
                "id": "voice_msg",
                "leftValue": "={{ $json.message.voice }}",
                "operator": {"type": "object", "operation": "exists"}
            },
            {
                "id": "image_msg",
                "leftValue": "={{ $json.message.photo }}",
                "operator": {"type": "array", "operation": "notEmpty"}
            },
            {
                "id": "document_msg",
                "leftValue": "={{ $json.message.document }}",
                "operator": {"type": "object", "operation": "exists"}
            },
            # Default text
            {
                "id": "text_msg",
                "leftValue": "={{ $json.message.text }}",
                "operator": {"type": "string", "operation": "exists"}
            }
        ],
        "combinator": "or"
    }
    
    # Update router node
    router_node['parameters']['conditions'] = fixed_conditions
    
    print(f"🔧 Updated router with {len(fixed_conditions['conditions'])} conditions:")
    for i, cond in enumerate(fixed_conditions['conditions']):
        condition_id = cond.get('id', f'cond_{i}')
        print(f"  {i}: {condition_id} - {cond['leftValue']} {cond['operator']['operation']}")
    
    # Fix connections - router should have 6 outputs
    connections = workflow.get('connections', {})
    router_name = router_node['name']
    
    if router_name in connections:
        current_outputs = len(connections[router_name].get('main', []))
        print(f"📡 Current router outputs: {current_outputs}")
    else:
        print("📡 No router connections found")
        connections[router_name] = {"main": []}
    
    # Ensure router has 6 outputs (one per condition)
    router_outputs = []
    input_processor_name = "Enhanced Input Processor"
    
    for i in range(6):  # 6 conditions = 6 outputs
        router_outputs.append([{"node": input_processor_name, "type": "main", "index": 0}])
    
    connections[router_name]["main"] = router_outputs
    
    print(f"🔗 Fixed router connections: {len(router_outputs)} outputs -> {input_processor_name}")
    
    # Clean workflow data for update (minimal fields only)
    clean_workflow = {
        "name": workflow["name"],
        "nodes": workflow["nodes"], 
        "connections": workflow["connections"],
        "settings": workflow.get("settings", {})
    }
    
    # Update workflow
    print("\n🚀 Updating workflow...")
    success, result = api.update_workflow(workflow_id, clean_workflow)
    
    if success:
        print("✅ Enhanced AI Agent router fixed!")
        print(f"🌐 View: {api.base_url}/workflow/{workflow_id}")
        print("\n📋 Router now handles:")
        print("  0: /search commands")
        print("  1: /files commands") 
        print("  2: Voice messages")
        print("  3: Image messages")
        print("  4: Document messages")
        print("  5: Text messages (default)")
    else:
        print(f"❌ Update failed: {result}")

if __name__ == "__main__":
    main()