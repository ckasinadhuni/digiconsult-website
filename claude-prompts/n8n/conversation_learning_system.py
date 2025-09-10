#!/usr/bin/env python3

"""
Conversation Learning System - Analyzes past prompts/responses for error patterns
Learns from mistakes to avoid repeating them in future workflow generations
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class ConversationLearningSystem:
    def __init__(self):
        self.learning_data_path = Path(__file__).parent / "learning_data.json"
        self.error_patterns = defaultdict(list)
        self.success_patterns = defaultdict(list)
        self.user_feedback_patterns = []
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load existing learning data"""
        if self.learning_data_path.exists():
            with open(self.learning_data_path, 'r') as f:
                data = json.load(f)
                self.error_patterns = defaultdict(list, data.get('error_patterns', {}))
                self.success_patterns = defaultdict(list, data.get('success_patterns', {}))
                self.user_feedback_patterns = data.get('user_feedback_patterns', [])
    
    def save_learning_data(self):
        """Save learning data to file"""
        data = {
            'error_patterns': dict(self.error_patterns),
            'success_patterns': dict(self.success_patterns),
            'user_feedback_patterns': self.user_feedback_patterns,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.learning_data_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def analyze_error_patterns_from_session(self):
        """Analyze error patterns from current session based on our conversation"""
        
        # Key error patterns identified from our session
        identified_errors = [
            {
                'error_type': 'api_endpoint_assumption',
                'pattern': 'Using /api/v1/node-types instead of /types/nodes.json',
                'impact': 'high',
                'occurrence_count': 3,
                'fix': 'Always validate API endpoints before use',
                'prevention': 'Check n8n docs or test endpoint first'
            },
            {
                'error_type': 'node_version_mismatch',
                'pattern': 'Assuming @n8n/n8n-nodes-base.telegramTrigger format instead of n8n-nodes-base.telegramTrigger',
                'impact': 'high', 
                'occurrence_count': 5,
                'fix': 'Use exact node names from /types/nodes.json endpoint',
                'prevention': 'Always validate node types before workflow creation'
            },
            {
                'error_type': 'langchain_availability_assumption',
                'pattern': 'Concluded LangChain nodes unavailable without proper validation',
                'impact': 'critical',
                'occurrence_count': 2,
                'fix': 'Proper endpoint validation revealed 103 LangChain nodes available',
                'prevention': 'Never assume node availability - always validate'
            },
            {
                'error_type': 'docker_compose_compatibility',
                'pattern': 'docker-compose 1.29.2 incompatible with Docker 27.5.1 causing ContainerConfig errors',
                'impact': 'high',
                'occurrence_count': 1,
                'fix': 'Use direct docker commands or upgrade docker-compose',
                'prevention': 'Check version compatibility before container operations'
            },
            {
                'error_type': 'custom_generator_complexity',
                'pattern': 'Building complex Python generators instead of using proven community templates',
                'impact': 'medium',
                'occurrence_count': 1,
                'fix': 'Switch to n8n community template approach',
                'prevention': 'Research existing solutions before building from scratch'
            }
        ]
        
        # User feedback patterns from session
        user_feedback = [
            {
                'feedback_type': 'validation_reminder',
                'content': 'Pull node types everytime you are generating a new workflow. Validate each node every time!',
                'importance': 'critical',
                'implementation': 'Added template_validator.py with mandatory pre-deployment validation'
            },
            {
                'feedback_type': 'approach_correction',
                'content': 'Use community template approach instead of custom generators',
                'importance': 'high',
                'implementation': 'Researched n8n.io/workflows community templates'
            },
            {
                'feedback_type': 'preference_ollama',
                'content': 'Use ollama in local instance running, use that first, langchain comes when that cant be used',
                'importance': 'medium',
                'implementation': 'Prioritize local Ollama over external services'
            },
            {
                'feedback_type': 'thorough_validation',
                'content': 'Be thorough and get on with your next tasks after validation',
                'importance': 'high',
                'implementation': 'Added comprehensive pre-deployment node validation'
            }
        ]
        
        return identified_errors, user_feedback
    
    def extract_success_patterns(self):
        """Extract successful approaches from the session"""
        
        success_patterns = [
            {
                'success_type': 'proper_api_validation',
                'pattern': 'Using /types/nodes.json endpoint successfully retrieved 794 node types',
                'impact': 'high',
                'replication': 'Always use this endpoint for node validation'
            },
            {
                'success_type': 'template_validator_approach',
                'pattern': 'Created template_validator.py that prevents node compatibility issues',
                'impact': 'critical',
                'replication': 'Use validator before every workflow deployment'
            },
            {
                'success_type': 'langchain_discovery',
                'pattern': 'Found 103 LangChain nodes available, deployed working AI agent',
                'impact': 'critical',
                'replication': 'LangChain nodes work in n8nio/n8n:latest 1.107.3'
            },
            {
                'success_type': 'safe_docker_update',
                'pattern': 'Successfully updated n8n 1.106.3 → 1.107.3 with data preservation',
                'impact': 'high',
                'replication': 'Clean container state, preserve volumes, use direct docker commands'
            },
            {
                'success_type': 'multimodal_workflow_deployment',
                'pattern': 'Successfully deployed AI agent with multimodal Telegram input',
                'impact': 'high',
                'replication': 'Use validated nodes: telegramTrigger → code → langchain.agent → telegram'
            }
        ]
        
        return success_patterns
    
    def learn_from_session(self):
        """Learn from the entire session and update knowledge base"""
        
        print("🧠 CONVERSATION LEARNING SYSTEM")
        print("=" * 50)
        print("Analyzing session for error patterns and success strategies...")
        
        errors, feedback = self.analyze_error_patterns_from_session()
        successes = self.extract_success_patterns()
        
        # Store error patterns
        for error in errors:
            self.error_patterns[error['error_type']].append({
                'pattern': error['pattern'],
                'impact': error['impact'],
                'fix': error['fix'],
                'prevention': error['prevention'],
                'learned_on': datetime.now().isoformat()
            })
        
        # Store success patterns  
        for success in successes:
            self.success_patterns[success['success_type']].append({
                'pattern': success['pattern'],
                'impact': success['impact'],
                'replication': success['replication'],
                'learned_on': datetime.now().isoformat()
            })
        
        # Store user feedback
        for fb in feedback:
            self.user_feedback_patterns.append({
                'type': fb['feedback_type'],
                'content': fb['content'],
                'importance': fb['importance'],
                'implementation': fb['implementation'],
                'learned_on': datetime.now().isoformat()
            })
        
        self.save_learning_data()
        
        print(f"\n📊 LEARNING SUMMARY:")
        print(f"✅ Identified {len(errors)} error patterns")
        print(f"✅ Identified {len(successes)} success patterns")
        print(f"✅ Captured {len(feedback)} user feedback items")
        print(f"💾 Learning data saved to: {self.learning_data_path}")
        
        return {
            'errors_learned': len(errors),
            'successes_learned': len(successes),
            'feedback_captured': len(feedback)
        }
    
    def generate_prevention_checklist(self):
        """Generate checklist to prevent future errors"""
        
        checklist = [
            "🔍 MANDATORY PRE-WORKFLOW VALIDATION:",
            "  • Use /types/nodes.json endpoint to validate all nodes",
            "  • Run template_validator.py before deployment",
            "  • Verify exact node names and versions",
            "  • Test API endpoints before assuming they work",
            "",
            "🎯 WORKFLOW CREATION PRIORITIES:",
            "  • Check n8n community templates first",
            "  • Use local services (Ollama) before external",
            "  • Validate LangChain node availability",
            "  • Preserve existing credentials and data",
            "",
            "⚠️ DOCKER/INFRASTRUCTURE:",
            "  • Check version compatibility before updates",
            "  • Preserve data volumes during container changes",
            "  • Use direct docker commands if compose fails",
            "",
            "👤 USER FEEDBACK INTEGRATION:",
            "  • Always validate user requirements thoroughly",
            "  • Implement feedback immediately in workflow",
            "  • Ask for clarification on assumptions"
        ]
        
        return "\n".join(checklist)
    
    def get_recommendations_for_task(self, task_type):
        """Get specific recommendations based on learned patterns"""
        
        recommendations = {
            'workflow_creation': [
                "Use template_validator.py BEFORE creating any workflow",
                "Check /types/nodes.json for exact node names",
                "Prefer community templates over custom generation",
                "Validate LangChain nodes are available (103 found in current instance)"
            ],
            'api_integration': [
                "Use /types/nodes.json not /api/v1/node-types",
                "Test endpoints before making assumptions",
                "Handle both 200 and 404 responses gracefully"
            ],
            'docker_operations': [
                "Check docker/docker-compose version compatibility",
                "Clean container state for image transitions",
                "Preserve data volumes during updates"
            ]
        }
        
        return recommendations.get(task_type, ["No specific recommendations for this task type"])

def main():
    """Test the learning system"""
    learning_system = ConversationLearningSystem()
    
    # Learn from current session
    results = learning_system.learn_from_session()
    
    # Generate prevention checklist
    print(f"\n📋 PREVENTION CHECKLIST FOR FUTURE SESSIONS:")
    print(learning_system.generate_prevention_checklist())
    
    # Show task-specific recommendations
    print(f"\n💡 WORKFLOW CREATION RECOMMENDATIONS:")
    for rec in learning_system.get_recommendations_for_task('workflow_creation'):
        print(f"  • {rec}")

if __name__ == "__main__":
    main()