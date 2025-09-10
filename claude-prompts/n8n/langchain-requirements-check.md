# LangChain Node Requirements Checker

## MANDATORY CHECK: Does this workflow require LangChain nodes?

**⚠️ BEFORE GENERATING ANY WORKFLOW - ASK THIS:**

### Features That REQUIRE LangChain nodes:
- [ ] **AI Agent orchestration** (unified decision making)
- [ ] **Conversation memory** (per-session context retention)  
- [ ] **Multi-tool integration** (calculator + web + code under one agent)
- [ ] **Local LLM with conversation flow** (Ollama with memory)
- [ ] **Context engineering automation** (window management, compression)

### Current n8n Environment Status:
- **Version:** 1.107.3 (official n8nio/n8n:latest)
- **LangChain Nodes:** ❌ NOT AVAILABLE
- **AI-Beta Image Required:** docker.n8n.io/n8nio/n8n:ai-beta

## Workflow Architecture Decision Tree:

```
Does workflow need AI Agent features?
├─ YES → Requires LangChain → Use ai-beta image OR redesign
└─ NO  → Use standard nodes → Continue with current setup
```

## Alternative Patterns for Non-LangChain Workflows:

### 1. Simple Ollama Integration:
```
HTTP Request Node → http://localhost:11434/api/generate
+ Manual prompt building in Code Node
+ Manual memory via Set/Memory nodes
```

### 2. Tool Routing:
```
Switch Node → Route to different tools
├─ Calculator → Math operations in Code Node
├─ Web Search → External API calls  
└─ Text Processing → Direct Ollama HTTP
```

### 3. Context Management:
```
Memory Node → Store conversation history
+ Code Node → Build context manually
+ Variable Node → Session management
```

## WARNING FLAGS:
- Any workflow using `@n8n/n8n-nodes-langchain.*` nodes
- Multi-tool AI assistants
- Conversation-aware bots
- Context engineering implementations

## SOLUTION PATH:
1. **Identify LangChain dependency** early in design
2. **Offer alternatives** using standard nodes
3. **Document upgrade path** to ai-beta image if needed