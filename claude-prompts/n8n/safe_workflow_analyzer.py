#!/usr/bin/env python3

"""
Safe workflow analyzer - no more Traceback errors
"""

import json
import requests

def safe_get(obj, key, default=None):
    """Safely get value from dict/object"""
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        elif hasattr(obj, key):
            return getattr(obj, key, default)
        else:
            return default
    except:
        return default

def safe_len(obj):
    """Safely get length"""
    try:
        return len(obj) if obj else 0
    except:
        return 0

def analyze_workflow():
    """Comprehensive workflow analysis with error handling"""
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Config load error: {e}")
        return

    headers = {'X-N8N-API-KEY': config['api_key']}
    workflow_id = 'jyskZP1sldP7NwYA'
    
    try:
        response = requests.get(f"{config['base_url']}/api/v1/workflows/{workflow_id}", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            return
            
        # Parse response safely
        try:
            workflow_data = response.json()
            # Handle both wrapped and direct responses
            if isinstance(workflow_data, dict) and 'data' in workflow_data:
                workflow = workflow_data['data']
            else:
                workflow = workflow_data
        except Exception as e:
            print(f"❌ JSON parse error: {e}")
            return
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return

    print('🔍 COMPREHENSIVE WORKFLOW ANALYSIS (SAFE)')
    print('=' * 60)
    
    # Safe workflow info extraction
    name = safe_get(workflow, 'name', 'Unknown')
    nodes = safe_get(workflow, 'nodes', [])
    active = safe_get(workflow, 'active', False)
    connections = safe_get(workflow, 'connections', {})
    
    print(f'Name: {name}')
    print(f'Total Nodes: {safe_len(nodes)}')
    print(f'Active: {active}')
    print()

    if not nodes:
        print("❌ No nodes found in workflow")
        return

    # Node analysis
    print('📊 NODE ANALYSIS:')
    print('-' * 40)
    
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            print(f"  {i}: Invalid node type")
            continue
            
        node_name = safe_get(node, 'name', f'Node_{i}')
        node_type = safe_get(node, 'type', 'unknown')
        node_version = safe_get(node, 'typeVersion', '?')
        
        print(f'  {i+1}. {node_name}')
        print(f'     Type: {node_type} v{node_version}')
        
        # Router analysis
        if 'switch' in node_type or 'router' in node_name.lower():
            params = safe_get(node, 'parameters', {})
            mode = safe_get(params, 'mode', 'NOT_SET')
            print(f'     Mode: {mode}')
            
            rules = safe_get(params, 'rules', {})
            if isinstance(rules, dict):
                values = safe_get(rules, 'values', [])
                print(f'     Rules: {safe_len(values)}')
                
                for j, rule in enumerate(values):
                    if isinstance(rule, dict):
                        output_key = safe_get(rule, 'outputKey', f'output_{j}')
                        conditions = safe_get(rule, 'conditions', {})
                        if isinstance(conditions, dict):
                            cond_list = safe_get(conditions, 'conditions', [])
                            if cond_list and isinstance(cond_list[0], dict):
                                first_cond = cond_list[0]
                                left_val = safe_get(first_cond, 'leftValue', '?')
                                operator = safe_get(first_cond, 'operator', {})
                                operation = safe_get(operator, 'operation', '?')
                                print(f'       {j}: {output_key} - {left_val} {operation}')
            
        # AI Agent analysis  
        elif 'langchain.agent' in node_type:
            params = safe_get(node, 'parameters', {})
            agent_type = safe_get(params, 'agent', 'NOT_SET')
            options = safe_get(params, 'options', {})
            system_msg = safe_get(options, 'systemMessage', '')
            print(f'     Agent: {agent_type}')
            print(f'     System msg: {safe_len(system_msg)} chars')
            
        # Vector store analysis
        elif 'vectorStore' in node_type:
            params = safe_get(node, 'parameters', {})
            collection = safe_get(params, 'collectionName', 'NOT_SET')
            url = safe_get(params, 'qdrantUrl', 'NOT_SET')
            print(f'     Collection: {collection}')
            print(f'     URL: {url}')
            
        # Tool analysis
        elif 'tool' in node_type.lower() or 'Tool' in node_type:
            params = safe_get(node, 'parameters', {})
            tool_name = safe_get(params, 'name', 'NOT_SET')
            description = safe_get(params, 'description', 'NOT_SET')
            desc_short = description[:50] + '...' if safe_len(description) > 50 else description
            print(f'     Tool: {tool_name}')
            print(f'     Desc: {desc_short}')
        
        print()

    # Connection analysis
    print('🔗 CONNECTIONS:')
    print('-' * 20)
    
    if isinstance(connections, dict):
        for source_name, conn_data in connections.items():
            if isinstance(conn_data, dict):
                print(f'{source_name}:')
                for conn_type, target_groups in conn_data.items():
                    if isinstance(target_groups, list):
                        print(f'  {conn_type}: {safe_len(target_groups)} outputs')
                        for i, target_group in enumerate(target_groups):
                            if isinstance(target_group, list):
                                for target in target_group:
                                    if isinstance(target, dict):
                                        target_node = safe_get(target, 'node', '?')
                                        target_type = safe_get(target, 'type', '?')
                                        print(f'    [{i}] -> {target_node} ({target_type})')
                print()
    
    print('✅ Analysis completed without errors')

if __name__ == "__main__":
    analyze_workflow()