#!/usr/bin/env python3

"""
n8n AI Agent Patterns Based on 2025 Best Practices
Implements the 4 core architectural patterns with context engineering optimization
"""

from context_engineering import ContextEngineeringPatterns

class AIAgentPatterns:
    """
    Based on n8n's 2025 AI Agentic Workflow patterns with context engineering:
    1. Chained Requests Pattern - Pipeline memory with stage-focused context
    2. Single Agent Pattern - Persistent session memory with role-focused context
    3. Multi-Agent with Gatekeeper Pattern - Distributed shared memory with coordination-focused context
    4. Multi-Agent Teams Pattern - Collaborative memory with team-focused context
    
    Each pattern now includes:
    - Context-engineered prompts with strategic information placement
    - Optimized memory management based on workflow type
    - Dynamic context assembly and compression
    - Context quality evaluation
    """
    
    @staticmethod
    def chained_requests_pattern(credentials, services, **kwargs):
        """
        Chained Requests Pattern with Context Engineering:
        - Rigid logic with flexible components
        - Multi-stage processing with context continuity
        - Different AI models for specific tasks
        - Pipeline memory maintaining context across stages
        """
        context_config = ContextEngineeringPatterns.get_workflow_context_optimization("chained_requests")
        
        return {
            "pattern_name": "Chained Requests",
            "description": "Rigid logic with flexible AI components",
            "nodes": [
                {
                    "type": "trigger", 
                    "node": "@n8n/n8n-nodes-base.webhook",
                    "purpose": "input_receiver"
                },
                {
                    "type": "ai_processor",
                    "node": "@n8n/n8n-nodes-langchain.agent",
                    "purpose": "initial_processing",
                    "agent_type": "conversationalAgent"
                },
                {
                    "type": "ai_processor", 
                    "node": "@n8n/n8n-nodes-langchain.agent",
                    "purpose": "specialized_processing",
                    "agent_type": "toolsAgent"
                },
                {
                    "type": "context_assembly",
                    "node": "@n8n/n8n-nodes-base.code",
                    "purpose": "context_optimization",
                    "implementation": ContextEngineeringPatterns.create_dynamic_context_assembler()
                },
                {
                    "type": "memory",
                    "node": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
                    "purpose": "pipeline_state_tracking",
                    "config": ContextEngineeringPatterns.get_context_optimized_memory("conversation"),
                    "context_window_size": context_config["context_window_size"],
                    "compression_threshold": context_config["compression_threshold"]
                },
                {
                    "type": "context_evaluator",
                    "node": "@n8n/n8n-nodes-base.code",
                    "purpose": "context_quality_check",
                    "implementation": ContextEngineeringPatterns.create_context_quality_evaluator()
                },
                {
                    "type": "output",
                    "node": "@n8n/n8n-nodes-base.httpRequest",
                    "purpose": "response_delivery"
                }
            ],
            "flow": "linear_chain",
            "complexity": "medium",
            "use_cases": ["content_processing", "data_analysis", "document_workflows"],
            "context_strategy": context_config,
            "prompt_templates": ContextEngineeringPatterns.generate_context_optimized_prompt(
                "Pipeline Processor",
                "Process input through sequential stages with context continuity"
            )
        }
    
    @staticmethod
    def single_agent_pattern(credentials, services, **kwargs):
        """
        Single Agent Pattern with Context Engineering:
        - One central agent maintaining workflow state
        - Can query multiple tools with context awareness
        - Maintains optimized context across interactions
        - Uses persistent session memory with user modeling
        """
        context_config = ContextEngineeringPatterns.get_workflow_context_optimization("single_agent")
        
        return {
            "pattern_name": "Single Agent",
            "description": "Central agent with multiple tools",
            "nodes": [
                {
                    "type": "trigger",
                    "node": "@n8n/n8n-nodes-base.manualTrigger",
                    "purpose": "workflow_start"
                },
                {
                    "type": "central_agent",
                    "node": "@n8n/n8n-nodes-langchain.agent",
                    "purpose": "main_processor",
                    "agent_type": "conversationalAgent",
                    "tools": ["web_search", "calculator", "code_interpreter"]
                },
                {
                    "type": "tool_nodes",
                    "nodes": [
                        {"node": "@n8n/n8n-nodes-langchain.toolHttpRequest", "purpose": "web_access"},
                        {"node": "@n8n/n8n-nodes-langchain.toolCalculator", "purpose": "calculations"},
                        {"node": "@n8n/n8n-nodes-langchain.toolCode", "purpose": "code_execution"}
                    ]
                },
                {
                    "type": "context_assembly",
                    "node": "@n8n/n8n-nodes-base.code",
                    "purpose": "dynamic_context_management",
                    "implementation": ContextEngineeringPatterns.create_dynamic_context_assembler()
                },
                {
                    "type": "memory", 
                    "node": "@n8n/n8n-nodes-langchain.memoryRedisChat",
                    "purpose": "persistent_conversation_context",
                    "config": ContextEngineeringPatterns.get_context_optimized_memory("persistent_session"),
                    "context_window_size": context_config["context_window_size"],
                    "user_modeling": True
                },
                {
                    "type": "context_compressor",
                    "node": "@n8n/n8n-nodes-langchain.agent",
                    "purpose": "memory_optimization",
                    "implementation": ContextEngineeringPatterns.create_context_compression_node()
                }
            ],
            "flow": "hub_and_spoke",
            "complexity": "low",
            "use_cases": ["personal_assistant", "customer_support", "information_retrieval"],
            "context_strategy": context_config,
            "prompt_templates": ContextEngineeringPatterns.generate_context_optimized_prompt(
                "Personal Assistant",
                "Provide helpful assistance using context awareness and memory continuity"
            )
        }
    
    @staticmethod
    def multi_agent_gatekeeper_pattern(credentials, services, **kwargs):
        """
        Multi-Agent with Gatekeeper Pattern with Context Engineering:
        - Centralized control with distributed expertise
        - Hierarchical structure with shared context management
        - Gatekeeper coordinates specialized sub-agents with context awareness
        - Distributed memory architecture for agent coordination
        """
        context_config = ContextEngineeringPatterns.get_workflow_context_optimization("multi_agent_gatekeeper")
        
        return {
            "pattern_name": "Multi-Agent Gatekeeper",
            "description": "Supervisor agent coordinating specialists",
            "nodes": [
                {
                    "type": "trigger",
                    "node": "@n8n/n8n-nodes-base.webhook",
                    "purpose": "request_entry"
                },
                {
                    "type": "gatekeeper_agent",
                    "node": "@n8n/n8n-nodes-langchain.agent",
                    "purpose": "request_routing",
                    "agent_type": "conversationalAgent",
                    "role": "supervisor"
                },
                {
                    "type": "routing_logic",
                    "node": "@n8n/n8n-nodes-base.switch",
                    "purpose": "agent_selection"
                },
                {
                    "type": "specialist_agents",
                    "nodes": [
                        {
                            "node": "@n8n/n8n-nodes-langchain.agent",
                            "purpose": "data_specialist",
                            "agent_type": "toolsAgent",
                            "specialization": "data_analysis"
                        },
                        {
                            "node": "@n8n/n8n-nodes-langchain.agent", 
                            "purpose": "content_specialist",
                            "agent_type": "conversationalAgent",
                            "specialization": "content_creation"
                        },
                        {
                            "node": "@n8n/n8n-nodes-langchain.agent",
                            "purpose": "technical_specialist", 
                            "agent_type": "sqlAgent",
                            "specialization": "database_queries"
                        }
                    ]
                },
                {
                    "type": "context_coordinator",
                    "node": "@n8n/n8n-nodes-base.code",
                    "purpose": "shared_context_management",
                    "implementation": ContextEngineeringPatterns.create_dynamic_context_assembler()
                },
                {
                    "type": "distributed_memory",
                    "node": "@n8n/n8n-nodes-langchain.memoryZep",
                    "purpose": "agent_coordination_memory",
                    "config": ContextEngineeringPatterns.get_context_optimized_memory("long_term_learning"),
                    "context_sharing": True,
                    "agent_specialization_tracking": True
                },
                {
                    "type": "aggregator",
                    "node": "@n8n/n8n-nodes-base.merge",
                    "purpose": "context_aware_response_consolidation"
                }
            ],
            "flow": "hierarchical",
            "complexity": "high", 
            "use_cases": ["complex_business_processes", "multi_domain_analysis", "enterprise_workflows"],
            "context_strategy": context_config,
            "prompt_templates": ContextEngineeringPatterns.generate_context_optimized_prompt(
                "Supervisor Agent",
                "Coordinate specialist agents using shared context and distributed expertise"
            )
        }
    
    @staticmethod
    def multi_agent_teams_pattern(credentials, services, **kwargs):
        """
        Multi-Agent Teams Pattern with Context Engineering:
        - Highly flexible architecture with collaborative memory
        - Distributed decision-making with shared context
        - Complex inter-agent interactions with context awareness
        - Team memory architecture for collaborative learning
        """
        context_config = ContextEngineeringPatterns.get_workflow_context_optimization("multi_agent_teams")
        
        return {
            "pattern_name": "Multi-Agent Teams",
            "description": "Collaborative agents with peer interactions",
            "nodes": [
                {
                    "type": "trigger",
                    "node": "@n8n/n8n-nodes-base.scheduleTrigger",
                    "purpose": "workflow_initiation"
                },
                {
                    "type": "coordinator",
                    "node": "@n8n/n8n-nodes-base.code",
                    "purpose": "task_distribution"
                },
                {
                    "type": "agent_team",
                    "nodes": [
                        {
                            "node": "@n8n/n8n-nodes-langchain.agent",
                            "purpose": "researcher_agent",
                            "agent_type": "conversationalAgent",
                            "tools": ["web_search", "document_retrieval"]
                        },
                        {
                            "node": "@n8n/n8n-nodes-langchain.agent",
                            "purpose": "analyst_agent", 
                            "agent_type": "toolsAgent",
                            "tools": ["calculator", "data_analysis"]
                        },
                        {
                            "node": "@n8n/n8n-nodes-langchain.agent",
                            "purpose": "writer_agent",
                            "agent_type": "conversationalAgent", 
                            "tools": ["text_generation", "formatting"]
                        }
                    ]
                },
                {
                    "type": "collaboration_nodes",
                    "nodes": [
                        {"node": "@n8n/n8n-nodes-base.merge", "purpose": "information_sharing"},
                        {"node": "@n8n/n8n-nodes-base.itemLists", "purpose": "task_tracking"},
                        {"node": "@n8n/n8n-nodes-langchain.memoryBufferWindow", "purpose": "shared_context"}
                    ]
                },
                {
                    "type": "team_memory",
                    "node": "@n8n/n8n-nodes-langchain.memoryZep",
                    "purpose": "collaborative_team_memory",
                    "config": ContextEngineeringPatterns.get_context_optimized_memory("long_term_learning"),
                    "team_learning": True,
                    "knowledge_sharing": True
                },
                {
                    "type": "context_synchronizer",
                    "node": "@n8n/n8n-nodes-base.code",
                    "purpose": "team_context_coordination",
                    "implementation": ContextEngineeringPatterns.create_dynamic_context_assembler()
                },
                {
                    "type": "quality_control",
                    "node": "@n8n/n8n-nodes-langchain.agent",
                    "purpose": "context_aware_output_validation",
                    "agent_type": "conversationalAgent",
                    "context_evaluation": True
                }
            ],
            "flow": "networked",
            "complexity": "very_high",
            "use_cases": ["research_projects", "content_production", "complex_problem_solving"],
            "context_strategy": context_config,
            "prompt_templates": ContextEngineeringPatterns.generate_context_optimized_prompt(
                "Collaborative Team Member",
                "Work collaboratively with team members using shared context and distributed knowledge"
            )
        }
    
    @staticmethod
    def get_context_enhanced_pattern_recommendations(use_case, complexity_preference="medium", context_requirements=None):
        """Get recommended pattern with context engineering considerations"""
        recommendations = {
            "simple_automation": "single_agent_pattern",
            "content_processing": "chained_requests_pattern", 
            "business_workflows": "multi_agent_gatekeeper_pattern",
            "research_analysis": "multi_agent_teams_pattern",
            "customer_support": "single_agent_pattern",
            "data_pipeline": "chained_requests_pattern",
            "enterprise_solution": "multi_agent_gatekeeper_pattern",
            "conversational_ai": "single_agent_pattern",
            "document_processing": "chained_requests_pattern",
            "multi_domain_expertise": "multi_agent_gatekeeper_pattern",
            "collaborative_research": "multi_agent_teams_pattern"
        }
        
        # Context-aware recommendations
        context_based_recommendations = {
            "high_memory_requirements": "multi_agent_teams_pattern",
            "real_time_context": "single_agent_pattern",
            "cross_session_continuity": "multi_agent_gatekeeper_pattern",
            "collaborative_memory": "multi_agent_teams_pattern"
        }
        
        complexity_mapping = {
            "low": ["single_agent_pattern"],
            "medium": ["single_agent_pattern", "chained_requests_pattern"],
            "high": ["chained_requests_pattern", "multi_agent_gatekeeper_pattern"],
            "very_high": ["multi_agent_teams_pattern"]
        }
        
        recommended = recommendations.get(use_case, "single_agent_pattern")
        
        # Apply context-based recommendations if specified
        if context_requirements:
            for req in context_requirements:
                if req in context_based_recommendations:
                    recommended = context_based_recommendations[req]
                    break
        
        # Check if recommended pattern matches complexity preference
        if recommended not in complexity_mapping.get(complexity_preference, []):
            # Fall back to complexity-appropriate pattern
            recommended = complexity_mapping[complexity_preference][0]
        
        return {
            "recommended_pattern": recommended,
            "context_optimization": ContextEngineeringPatterns.get_workflow_context_optimization(recommended.replace("_pattern", "")),
            "reasoning": f"Selected {recommended} based on use case '{use_case}', complexity '{complexity_preference}', and context requirements {context_requirements}"
        }