#!/usr/bin/env python3

"""
Context Engineering Best Practices for n8n LLM Workflows (2025)
Implements advanced context optimization, memory management, and prompt engineering
"""

class ContextEngineeringPatterns:
    """
    Context Engineering: The science of organizing, assembling, and optimizing 
    all forms of context fed into LLMs to maximize performance
    
    Key Principles (2025):
    1. Holistic context management over simple prompt crafting
    2. Dynamic context assembly with strategic information placement
    3. Multi-layered memory architecture 
    4. Context compression and optimization
    5. Workflow orchestration with specialized contexts
    """
    
    @staticmethod
    def get_context_optimized_memory(memory_type="conversation", persistence_level="session"):
        """
        Generate optimized memory configuration based on context engineering best practices
        
        Memory Hierarchy (2025 Best Practices):
        - Short-term: Buffer window for immediate context
        - Long-term: Persistent storage for cross-session memory
        - Working: Compressed summaries of relevant history
        - Meta: Context about context (conversation patterns, user preferences)
        """
        
        memory_configs = {
            "conversation": {
                "node": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
                "parameters": {
                    "windowSize": 10,  # Optimized for context window efficiency
                    "returnMessages": True,
                    "inputKey": "input",
                    "outputKey": "output",
                    "contextCompression": True  # Enable automatic context compression
                },
                "description": "Windowed memory with context compression for efficient conversations"
            },
            
            "persistent_session": {
                "node": "@n8n/n8n-nodes-langchain.memoryRedisChat",
                "parameters": {
                    "sessionTTL": 3600,  # 1 hour session memory
                    "maxTokens": 4000,   # Context window optimization
                    "compressionRatio": 0.3,  # Compress to 30% of original size
                    "summaryPrompt": "Compress the following conversation maintaining key context and user intent"
                },
                "description": "Redis-backed session memory with intelligent compression"
            },
            
            "long_term_learning": {
                "node": "@n8n/n8n-nodes-langchain.memoryZep",
                "parameters": {
                    "sessionId": "{{ $workflow.id }}-{{ $node.id }}",
                    "memoryKey": "history",
                    "longTermMemory": True,
                    "userMemory": True,  # Track user preferences and patterns
                    "contextAware": True,  # Enable context-aware retrieval
                    "vectorStore": True  # Use vector similarity for context retrieval
                },
                "description": "Long-term memory with user modeling and context-aware retrieval"
            }
        }
        
        return memory_configs.get(memory_type, memory_configs["conversation"])
    
    @staticmethod
    def generate_context_optimized_prompt(agent_role, task_context, memory_context=None):
        """
        Generate context-engineered prompts using 2025 best practices
        
        Context Engineering Structure:
        1. Role Definition (Clear identity and capabilities)
        2. Task Context (Specific current objective)
        3. Memory Context (Relevant historical information)
        4. Output Format (Structured response expectations)
        5. Constraints (Boundaries and limitations)
        """
        
        # Strategic information placement: Critical info at start and end
        prompt_template = {
            "system_prompt": f"""# {agent_role} - Context-Aware Assistant

## PRIMARY ROLE & CAPABILITIES
You are a {agent_role} with the following core competencies:
- Expert domain knowledge in your specialized area
- Context-aware reasoning and decision making  
- Memory-enhanced conversation continuity
- Structured output generation

## CURRENT TASK CONTEXT
{task_context}

## MEMORY & HISTORICAL CONTEXT
{memory_context or "No previous context available for this session."}

## RESPONSE FRAMEWORK
Please structure your response as:
1. **Context Analysis**: Brief assessment of the current situation
2. **Reasoning**: Your thought process and key considerations  
3. **Action/Response**: Your specific answer or recommended action
4. **Next Steps**: Suggested follow-up actions or questions

## CRITICAL CONSTRAINTS
- Stay within your role boundaries
- Prioritize accuracy over speed
- Ask for clarification when context is insufficient
- Maintain conversation continuity using provided memory

Remember: Quality context engineering leads to better outcomes than clever prompting.""",

            "user_prompt_template": """## Current Request
{{ $json.input || $json.message?.text || $json.query }}

## Additional Context
- Timestamp: {{ new Date().toISOString() }}
- Session ID: {{ $workflow.id }}
- User ID: {{ $json.user_id || 'anonymous' }}

## Context Quality Check
Before responding, verify:
1. Do you have sufficient context to provide a quality response?
2. Is there any ambiguity that requires clarification?
3. Are there relevant memories that should influence your response?

Proceed with your response using the framework above."""
        }
        
        return prompt_template
    
    @staticmethod
    def create_context_compression_node():
        """
        Create a context compression node using LLM-based summarization
        Implements the U-shaped context pattern optimization
        """
        return {
            "type": "@n8n/n8n-nodes-langchain.agent",
            "purpose": "context_compression",
            "parameters": {
                "agent": "conversationalAgent",
                "promptType": "define",
                "text": """You are a context compression specialist. Your job is to compress conversation history and context while preserving essential information.

COMPRESSION PRINCIPLES:
1. Preserve key facts, decisions, and user preferences
2. Maintain causal relationships between events
3. Keep emotional context and sentiment
4. Compress repetitive or redundant information
5. Highlight unresolved issues or pending actions

INPUT: Raw conversation/context history
OUTPUT: Compressed summary maintaining critical context

Format your compression as:
**Key Facts**: Bullet points of essential information
**User Profile**: Preferences, patterns, important details
**Current State**: What's happening now, pending actions
**Context Summary**: Brief narrative connecting the above

Compress the following context:
{{ $json.context_to_compress }}""",
                "options": {
                    "maxTokens": 500,  # Force concise compression
                    "temperature": 0.1  # Consistent, factual compression
                }
            },
            "description": "LLM-based context compression for memory optimization"
        }
    
    @staticmethod
    def create_context_quality_evaluator():
        """
        Create a node to evaluate context quality using RAGAS-style evaluation
        """
        return {
            "type": "@n8n/n8n-nodes-base.code",
            "purpose": "context_quality_evaluation",
            "parameters": {
                "jsCode": """// Context Quality Evaluation (inspired by RAGAS framework)

const evaluateContextQuality = (context, query, response) => {
    const metrics = {
        relevance: 0,
        completeness: 0,
        coherence: 0,
        factualConsistency: 0
    };
    
    // Relevance: How well does context relate to query
    const contextTokens = context.toLowerCase().split(/\\s+/);
    const queryTokens = query.toLowerCase().split(/\\s+/);
    const overlap = queryTokens.filter(token => contextTokens.includes(token)).length;
    metrics.relevance = Math.min(overlap / queryTokens.length, 1.0);
    
    // Completeness: Does context provide sufficient information
    const keyPhrases = ['because', 'therefore', 'however', 'specifically', 'for example'];
    const explanatoryPhrases = keyPhrases.filter(phrase => context.toLowerCase().includes(phrase)).length;
    metrics.completeness = Math.min(explanatoryPhrases / 3, 1.0);
    
    // Coherence: Is context logically structured
    const sentences = context.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const avgSentenceLength = sentences.reduce((sum, s) => sum + s.split(/\\s+/).length, 0) / sentences.length;
    metrics.coherence = avgSentenceLength > 5 && avgSentenceLength < 30 ? 0.8 : 0.4;
    
    // Overall score
    const overallScore = Object.values(metrics).reduce((sum, score) => sum + score, 0) / 4;
    
    return {
        json: {
            context_quality_score: overallScore,
            metrics: metrics,
            recommendation: overallScore > 0.7 ? 'Good context quality' : 
                           overallScore > 0.4 ? 'Context needs improvement' : 
                           'Poor context - consider compression or enhancement',
            timestamp: new Date().toISOString()
        }
    };
};

// Evaluate current context
const context = $json.context || '';
const query = $json.query || $json.input || '';
const response = $json.response || '';

return [evaluateContextQuality(context, query, response)];"""
            },
            "description": "Evaluates context quality using multiple metrics"
        }
    
    @staticmethod
    def create_dynamic_context_assembler():
        """
        Create a node that dynamically assembles optimal context based on current needs
        Implements strategic information placement and context window optimization
        """
        return {
            "type": "@n8n/n8n-nodes-base.code", 
            "purpose": "dynamic_context_assembly",
            "parameters": {
                "jsCode": """// Dynamic Context Assembly with Strategic Placement (2025 Best Practices)

const assembleOptimalContext = (data) => {
    const maxContextTokens = 3000; // Assume 4K context window with 1K buffer
    const criticalInfoWeight = 0.4; // 40% for critical info
    const recentInfoWeight = 0.3;   // 30% for recent context
    const relevantHistoryWeight = 0.3; // 30% for relevant history
    
    // Extract different types of context
    const criticalInfo = data.critical_context || '';
    const recentContext = data.recent_context || '';
    const historicalContext = data.historical_context || '';
    const userPreferences = data.user_preferences || '';
    const currentTask = data.current_task || '';
    
    // Token estimation (rough: 1 token ≈ 4 characters)
    const estimateTokens = (text) => Math.ceil(text.length / 4);
    
    // Prioritized context assembly using U-shaped pattern
    let assembledContext = '';
    let remainingTokens = maxContextTokens;
    
    // BEGINNING: Most critical information (high attention)
    const criticalSection = `=== CRITICAL CONTEXT ===
${criticalInfo}
${currentTask}

`;
    
    if (estimateTokens(criticalSection) < remainingTokens * criticalInfoWeight) {
        assembledContext += criticalSection;
        remainingTokens -= estimateTokens(criticalSection);
    }
    
    // MIDDLE: Recent context (medium attention - keep concise)
    const recentSection = `=== RECENT CONTEXT ===
${recentContext}

`;
    
    if (estimateTokens(recentSection) < remainingTokens * recentInfoWeight) {
        assembledContext += recentSection;
        remainingTokens -= estimateTokens(recentSection);
    }
    
    // END: Relevant history and preferences (high attention)
    const historySection = `=== RELEVANT BACKGROUND ===
${historicalContext}

=== USER PREFERENCES ===
${userPreferences}`;
    
    if (estimateTokens(historySection) < remainingTokens) {
        assembledContext += historySection;
    }
    
    // Context compression if too long
    if (estimateTokens(assembledContext) > maxContextTokens) {
        assembledContext = `=== COMPRESSED CONTEXT ===
CRITICAL: ${criticalInfo.substring(0, 500)}...
TASK: ${currentTask.substring(0, 300)}...
RECENT: ${recentContext.substring(0, 400)}...
BACKGROUND: ${historicalContext.substring(0, 300)}...`;
    }
    
    return {
        json: {
            assembled_context: assembledContext,
            context_stats: {
                estimated_tokens: estimateTokens(assembledContext),
                sections_included: ['critical', 'recent', 'historical', 'preferences'],
                optimization_applied: estimateTokens(assembledContext) > maxContextTokens,
                assembly_timestamp: new Date().toISOString()
            },
            context_quality_indicators: {
                has_critical_info: criticalInfo.length > 0,
                has_recent_context: recentContext.length > 0,
                has_user_preferences: userPreferences.length > 0,
                context_diversity_score: [criticalInfo, recentContext, historicalContext, userPreferences]
                    .filter(ctx => ctx.length > 0).length / 4
            }
        }
    };
};

// Process input data
const inputData = $json;
return [assembleOptimalContext(inputData)];"""
            },
            "description": "Dynamically assembles optimal context using strategic information placement"
        }
    
    @staticmethod
    def get_workflow_context_optimization(workflow_type="single_agent"):
        """
        Get context optimization strategy based on workflow type
        """
        
        optimizations = {
            "single_agent": {
                "memory_strategy": "persistent_session",
                "context_window_size": 4000,
                "compression_threshold": 0.8,
                "prompt_strategy": "role_focused",
                "memory_nodes": ["buffer_window", "user_preferences"]
            },
            
            "multi_agent_gatekeeper": {
                "memory_strategy": "distributed_shared",
                "context_window_size": 6000,  # Larger for coordination
                "compression_threshold": 0.6,  # More aggressive compression
                "prompt_strategy": "coordination_focused", 
                "memory_nodes": ["shared_context", "agent_specialization", "task_history"]
            },
            
            "multi_agent_teams": {
                "memory_strategy": "collaborative_memory",
                "context_window_size": 8000,  # Maximum for complex interactions
                "compression_threshold": 0.5,  # Most aggressive compression
                "prompt_strategy": "collaboration_focused",
                "memory_nodes": ["team_memory", "individual_memory", "shared_knowledge", "task_coordination"]
            },
            
            "chained_requests": {
                "memory_strategy": "pipeline_memory", 
                "context_window_size": 3000,  # Focused per stage
                "compression_threshold": 0.7,
                "prompt_strategy": "stage_focused",
                "memory_nodes": ["stage_results", "pipeline_state", "accumulated_context"]
            }
        }
        
        return optimizations.get(workflow_type, optimizations["single_agent"])