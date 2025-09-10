# 🤖 Intelligent n8n Workflow Generator with Context Engineering (2025)

> **Automated workflow generation with n8n's latest AI agent patterns, context engineering optimization, and 2025 best practices.**

## 📌 **Quick Access**: *"Create a new n8n workflow through Claude CLI automation"*

**→ See [QUICK-REFERENCE.md](QUICK-REFERENCE.md) for instant commands and solutions**  
**→ See [README-CLAUDE-CLI.md](README-CLAUDE-CLI.md) for comprehensive guide**

## 🚀 Features

- **🔄 Dynamic Best Practices**: Always uses latest n8n recommendations
- **🤖 AI Agent Patterns**: 4 proven architectures from n8n's 2025 guide
- **🔑 Smart Credential Management**: Auto-discovers and reuses existing credentials
- **📦 Community Node Support**: Discovers and integrates community nodes
- **⚡ Intelligent Caching**: Fast reruns with smart cache invalidation
- **🎯 One-Command Deploy**: Generate and deploy in single command

## 📁 Lean Structure

```
claude-prompts/n8n/
├── config.json          # API keys + essential config ONLY
├── generate             # Single intelligent generator script
├── templates/           # Minimal template logic (not full workflows)
│   ├── ai-agent-patterns.py
│   └── telegram-ai.py
└── cache/               # Temporary cached data (auto-managed)
```

## 🛠️ Setup

**One-time setup:**
```bash
# Your credentials are already stored in config.json
cd /home/ubuntu/claude-prompts/n8n
./generate --list-patterns  # Verify setup
```

## 🎯 Usage

### AI Agent Workflows (n8n 2025 Patterns)

```bash
# Single Agent - Customer support, personal assistant
./generate single-agent --deploy

# Chained Requests - Content processing, data analysis  
./generate chained-requests --deploy

# Multi-Agent Gatekeeper - Business workflows, multi-domain
./generate multi-agent-gatekeeper --deploy

# Multi-Agent Teams - Research, complex problem solving
./generate multi-agent-teams --deploy
```

### Classic Workflows

```bash
# Telegram AI Assistant (enhanced with voice/image)
./generate telegram-ai-assistant --deploy

# Webhook to Database Pipeline
./generate webhook-to-database --source=api --target=postgres --deploy

# Data Processing Pipeline
./generate data-processor --input=csv --ai=ollama --deploy

# Scheduled Automation
./generate scheduler --frequency=daily --action=backup --deploy
```

### Quick Commands

```bash
# List available patterns
./generate --list-patterns

# Generate without deploying (saves JSON locally)
./generate single-agent

# Generate and deploy in one command
./generate multi-agent-gatekeeper --deploy
```

## 🧠 AI Agent Patterns (n8n 2025)

### 1. **Single Agent Pattern**
- **Complexity**: Low
- **Architecture**: One central agent with multiple tools
- **Use Cases**: Customer support, personal assistant, information retrieval
- **Best For**: Simple automation, single domain expertise

### 2. **Chained Requests Pattern**
- **Complexity**: Medium  
- **Architecture**: Sequential AI processing pipeline
- **Use Cases**: Content processing, data analysis, document workflows
- **Best For**: Multi-stage processing, specialized AI models per stage

### 3. **Multi-Agent Gatekeeper Pattern**
- **Complexity**: High
- **Architecture**: Supervisor agent coordinating specialists
- **Use Cases**: Business workflows, multi-domain analysis, enterprise solutions
- **Best For**: Complex routing, specialized expertise needed

### 4. **Multi-Agent Teams Pattern**
- **Complexity**: Very High
- **Architecture**: Collaborative peer agents with distributed decision-making
- **Use Cases**: Research projects, content production, complex problem solving
- **Best For**: Creative collaboration, multi-perspective analysis

## 🔧 How It Works

### Intelligent Generation Process

1. **Dynamic Analysis**:
   - Fetches current n8n version and capabilities
   - Discovers available credentials automatically
   - Analyzes installed community nodes
   - Caches results for fast reruns

2. **Pattern Selection**:
   - Matches workflow type to optimal AI agent pattern
   - Considers complexity preferences
   - Applies n8n 2025 best practices automatically

3. **Smart Generation**:
   - Creates nodes with proper connections
   - Configures credentials automatically
   - Sets optimal parameters based on current practices
   - Positions nodes in logical layout

4. **One-Command Deploy**:
   - Generates workflow JSON
   - Deploys via n8n API
   - Activates workflow
   - Reports deployment status

### Credential Management

- **Stored Locally**: API keys, bot tokens (sensitive data)
- **Retrieved Dynamically**: Credential lists, node types, settings
- **Auto-Discovery**: Finds and reuses existing n8n credentials
- **Smart Caching**: 5-minute cache for credentials, 1-hour for node types

## 📊 Performance

- **Cold Start**: ~2-3 seconds (with API calls)
- **Warm Cache**: ~0.5 seconds (using cached data)
- **Generation**: ~1 second per workflow
- **Deployment**: ~3-5 seconds (API + activation)

## 🔒 Security

- **API Keys**: Stored in local config.json only
- **Credentials**: Retrieved from n8n, never stored locally
- **Cache**: Contains only non-sensitive metadata
- **Auto-Cleanup**: Cache expires automatically

## 🚦 Examples

### Business Process Automation
```bash
# Generate supervisor agent for invoice processing
./generate multi-agent-gatekeeper --deploy
# Creates: Receipt agent → Analysis agent → Approval agent → Database agent
```

### Research Assistant
```bash
# Generate collaborative research team
./generate multi-agent-teams --deploy  
# Creates: Researcher → Analyst → Writer → Quality Control
```

### Customer Support
```bash
# Generate single agent with multiple tools
./generate single-agent --deploy
# Creates: One agent with web search, knowledge base, escalation tools
```

## 📈 Extensibility

### Adding New Patterns

1. Edit `templates/ai-agent-patterns.py`
2. Add new pattern method
3. Register in pattern selection logic
4. Test with `./generate your-new-pattern`

### Adding New Workflow Types

1. Add detection logic in `generate_workflow_structure()`
2. Implement `_generate_your_workflow()` method
3. Test and deploy

### Community Node Integration

- **Auto-Discovery**: System finds installed community nodes
- **Smart Integration**: Suggests community nodes when relevant
- **Fallback Logic**: Uses built-in nodes if community nodes unavailable

## 🔄 Best Practices Applied

- **Error Workflows**: Enabled automatically when supported
- **Memory Management**: BufferWindow memory for conversational agents
- **Connection Types**: Proper `ai_languageModel` connections for LangChain
- **Node Versioning**: Uses latest compatible node versions
- **Positioning**: Logical node layout for readability
- **Tags**: Automatic tagging for workflow organization

## 🚨 Troubleshooting

```bash
# Check system status
curl http://localhost:5678/rest/settings  # n8n
curl http://localhost:8000/health         # faster-whisper  
curl http://localhost:11434/api/tags      # ollama

# Clear cache
rm -rf /home/ubuntu/claude-prompts/n8n/cache/*

# Regenerate workflow
./generate your-workflow-type  # Without --deploy to test JSON first
```

## 📝 Generated Files

- **Local JSON**: Saved as `generated-{type}-{timestamp}.json`
- **n8n Deployment**: Accessible via n8n interface
- **Cache Files**: Automatically managed in `cache/` directory
- **Logs**: Displayed in console with status indicators

---

**🎉 Ready to generate intelligent workflows with n8n's 2025 best practices!**