#!/usr/bin/env python3

"""
Template Validator - Validates n8n workflow templates against current instance
Ensures all nodes are compatible before importing any workflow
"""

import json
import requests
from pathlib import Path

class TemplateValidator:
    def __init__(self):
        self.config_path = Path(__file__).parent / "config.json"
        self.load_config()
        self.available_nodes = None
        
    def load_config(self):
        """Load configuration"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        self.headers = {
            "X-N8N-API-KEY": self.config["api_key"],
            "Content-Type": "application/json"
        }
        self.base_url = self.config["base_url"]
    
    def fetch_available_nodes(self):
        """Fetch all available node types from current n8n instance"""
        try:
            response = requests.get(f"{self.base_url}/types/nodes.json", timeout=10)
            if response.status_code == 200:
                nodes_data = response.json()
                # Create lookup dictionary: {node_name: {versions: [], displayName: ""}}
                self.available_nodes = {}
                
                for node in nodes_data:
                    name = node.get('name', '')
                    version = node.get('version', 1)
                    display_name = node.get('displayName', '')
                    
                    if name not in self.available_nodes:
                        self.available_nodes[name] = {
                            'versions': [],
                            'displayName': display_name
                        }
                    
                    # Handle both single versions and version arrays
                    if isinstance(version, list):
                        self.available_nodes[name]['versions'].extend(version)
                    else:
                        self.available_nodes[name]['versions'].append(version)
                
                # Remove duplicates and sort versions
                for name in self.available_nodes:
                    self.available_nodes[name]['versions'] = sorted(list(set(self.available_nodes[name]['versions'])))
                
                print(f"✅ Loaded {len(self.available_nodes)} available node types")
                return True
                
            else:
                print(f"❌ Failed to fetch nodes: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error fetching nodes: {e}")
            return False
    
    def validate_node(self, node_type, node_version):
        """Validate if a specific node type and version is available"""
        if not self.available_nodes:
            if not self.fetch_available_nodes():
                return False, "Could not fetch available nodes"
        
        if node_type not in self.available_nodes:
            return False, f"Node type '{node_type}' not available"
        
        available_versions = self.available_nodes[node_type]['versions']
        
        # Check if requested version is available
        if node_version not in available_versions:
            return False, f"Version {node_version} not available. Available: {available_versions}"
        
        return True, f"✅ Valid: {self.available_nodes[node_type]['displayName']} v{node_version}"
    
    def validate_workflow_json(self, workflow_json):
        """Validate entire workflow JSON for node compatibility"""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'node_validations': []
        }
        
        # Parse workflow if it's a string
        if isinstance(workflow_json, str):
            try:
                workflow_data = json.loads(workflow_json)
            except json.JSONError as e:
                validation_results['valid'] = False
                validation_results['errors'].append(f"Invalid JSON: {e}")
                return validation_results
        else:
            workflow_data = workflow_json
        
        # Check required workflow fields
        required_fields = ['name', 'nodes']
        for field in required_fields:
            if field not in workflow_data:
                validation_results['valid'] = False
                validation_results['errors'].append(f"Missing required field: {field}")
        
        # Validate each node
        nodes = workflow_data.get('nodes', [])
        for i, node in enumerate(nodes):
            node_name = node.get('name', f'Node {i+1}')
            node_type = node.get('type', '')
            node_version = node.get('typeVersion', 1)
            
            is_valid, message = self.validate_node(node_type, node_version)
            
            validation_result = {
                'node_name': node_name,
                'node_type': node_type,
                'requested_version': node_version,
                'valid': is_valid,
                'message': message
            }
            
            validation_results['node_validations'].append(validation_result)
            
            if not is_valid:
                validation_results['valid'] = False
                validation_results['errors'].append(f"Node '{node_name}': {message}")
        
        return validation_results
    
    def suggest_node_fix(self, node_type, requested_version):
        """Suggest compatible version for incompatible node"""
        if node_type not in self.available_nodes:
            # Try to find similar node types
            similar = [name for name in self.available_nodes.keys() if node_type.split('.')[-1] in name]
            if similar:
                return f"Node not found. Similar available: {similar[:3]}"
            return "Node type not available in this n8n instance"
        
        available_versions = self.available_nodes[node_type]['versions']
        closest_version = max([v for v in available_versions if v <= requested_version], default=None)
        
        if closest_version:
            return f"Use version {closest_version} instead of {requested_version}"
        else:
            return f"Use latest available version: {max(available_versions)}"
    
    def auto_fix_workflow(self, workflow_json):
        """Attempt to auto-fix workflow with compatible node versions"""
        if isinstance(workflow_json, str):
            workflow_data = json.loads(workflow_json)
        else:
            workflow_data = workflow_json.copy()
        
        fixes_applied = []
        
        for node in workflow_data.get('nodes', []):
            node_type = node.get('type', '')
            requested_version = node.get('typeVersion', 1)
            
            is_valid, message = self.validate_node(node_type, requested_version)
            
            if not is_valid and node_type in self.available_nodes:
                # Use highest available version
                available_versions = self.available_nodes[node_type]['versions']
                best_version = max(available_versions)
                
                if best_version != requested_version:
                    node['typeVersion'] = best_version
                    fixes_applied.append(f"Fixed {node.get('name', node_type)}: v{requested_version} → v{best_version}")
        
        return workflow_data, fixes_applied
    
    def print_validation_report(self, validation_results):
        """Print detailed validation report"""
        print("\n" + "="*60)
        print("WORKFLOW VALIDATION REPORT")
        print("="*60)
        
        if validation_results['valid']:
            print("✅ WORKFLOW IS COMPATIBLE")
        else:
            print("❌ WORKFLOW HAS COMPATIBILITY ISSUES")
        
        print(f"\n📊 NODE VALIDATION RESULTS:")
        for result in validation_results['node_validations']:
            status = "✅" if result['valid'] else "❌"
            print(f"{status} {result['node_name']}: {result['message']}")
        
        if validation_results['errors']:
            print(f"\n🚨 ERRORS ({len(validation_results['errors'])}):")
            for error in validation_results['errors']:
                print(f"  • {error}")
        
        if validation_results['warnings']:
            print(f"\n⚠️ WARNINGS ({len(validation_results['warnings'])}):")
            for warning in validation_results['warnings']:
                print(f"  • {warning}")
        
        print("="*60)

def main():
    """Test the validator"""
    validator = TemplateValidator()
    
    # Test basic node validation
    print("🔍 TESTING NODE VALIDATION")
    print("-" * 30)
    
    test_nodes = [
        ("n8n-nodes-base.manualTrigger", 1),
        ("n8n-nodes-base.set", 3.4),
        ("n8n-nodes-base.httpRequest", 4.2),
        ("n8n-nodes-base.code", 2),
        ("@n8n/n8n-nodes-langchain.agent", 1)  # This should fail
    ]
    
    for node_type, version in test_nodes:
        is_valid, message = validator.validate_node(node_type, version)
        print(f"{node_type} v{version}: {message}")
    
    print(f"\n📋 Available basic nodes:")
    basic_nodes = [name for name in validator.available_nodes.keys() 
                   if 'base.' in name and any(x in name for x in ['manual', 'set', 'http', 'code'])]
    for node in basic_nodes[:10]:
        versions = validator.available_nodes[node]['versions']
        print(f"  • {node}: versions {versions}")

if __name__ == "__main__":
    main()