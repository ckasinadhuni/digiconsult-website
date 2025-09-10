# 🤖 n8n Workflow Automation via Claude CLI

## Quick Reference: "Create a new n8n workflow through Claude CLI automation"

### 📋 Command Summary Table

| Command | Purpose | Context Engineering | Deployment | Prerequisites |
|---------|---------|---------------------|------------|---------------|
| `./generate --list-patterns` | List available AI agent patterns | ✅ Optimized | ❌ Info only | None |
| `./generate single-agent` | Personal assistant, customer support | 4K context, persistent memory | ❌ Local JSON | None |
| `./generate single-agent --deploy` | Deploy personal assistant workflow | 4K context, persistent memory | ✅ Auto-deploy + activate | n8n running |
| `./generate multi-agent-gatekeeper` | Business workflows, multi-domain analysis | 6K context, distributed memory | ❌ Local JSON | None |
| `./generate multi-agent-gatekeeper --deploy` | Deploy supervisor-specialist workflow | 6K context, distributed memory | ✅ Auto-deploy + activate | n8n running |
| `./generate multi-agent-teams` | Research projects, collaborative work | 8K context, collaborative memory | ❌ Local JSON | None |
| `./generate multi-agent-teams --deploy` | Deploy collaborative agent network | 8K context, collaborative memory | ✅ Auto-deploy + activate | n8n running |
| `./generate chained-requests` | Content processing, data pipelines | 3K context, pipeline memory | ❌ Local JSON | None |
| `./generate chained-requests --deploy` | Deploy sequential processing workflow | 3K context, pipeline memory | ✅ Auto-deploy + activate | n8n running |
| `./generate telegram-ai-assistant` | Telegram bot with AI capabilities | 4K context, session memory | ❌ Local JSON | Telegram credentials |
| `./generate telegram-ai-assistant --deploy` | Deploy Telegram AI bot | 4K context, session memory | ✅ Auto-deploy + activate | Telegram credentials + n8n |
| `./generate webhook-to-database --source=api --target=postgres` | API data ingestion to database | Standard context | ❌ Local JSON | Database credentials |
| `./generate data-processor --input=csv --ai=ollama` | Process files with AI analysis | AI-optimized context | ❌ Local JSON | File source |

---

### 🚀 High-Level Commands

#### **1. Quick Start (No Prerequisites)**
```bash
# List all available patterns
./generate --list-patterns

# Generate AI assistant (local file only)
./generate single-agent
```

#### **2. Production Deployment (Requires n8n)**
```bash
# Deploy context-engineered personal assistant
./generate single-agent --deploy

# Deploy business workflow coordinator  
./generate multi-agent-gatekeeper --deploy

# Deploy research collaboration team
./generate multi-agent-teams --deploy
```

#### **3. Specialized Workflows**
```bash
# Telegram AI bot (requires credentials)
./generate telegram-ai-assistant --deploy

# Data processing pipeline
./generate webhook-to-database --source=webhooks --target=postgresql --deploy

# Content processing chain
./generate chained-requests --ai=ollama --deploy
```

---

### ❓ Frequently Asked Questions

#### **Q: How do I create a new n8n workflow through Claude CLI automation?**

| Step | Action | Command | Expected Outcome |
|------|--------|---------|------------------|
| 1 | Check available patterns | `./generate --list-patterns` | Shows 4 AI agent patterns + use cases |
| 2 | Choose pattern for your use case | See **Pattern Selection Guide** below | - |
| 3 | Generate workflow | `./generate [pattern-name]` | Creates local JSON file |
| 4 | Deploy to n8n (optional) | `./generate [pattern-name] --deploy` | Auto-deploys + activates in n8n |

#### **Q: Which pattern should I choose?**

| Use Case | Recommended Pattern | Context Size | Memory Type | Complexity |
|----------|-------------------|--------------|-------------|------------|
| **Personal assistant, customer support** | `single-agent` | 4K tokens | Persistent session | Low |
| **Content processing, data analysis** | `chained-requests` | 3K tokens | Pipeline memory | Medium |
| **Business workflows, multi-domain** | `multi-agent-gatekeeper` | 6K tokens | Distributed shared | High |
| **Research projects, collaboration** | `multi-agent-teams` | 8K tokens | Collaborative memory | Very High |
| **Telegram bot** | `telegram-ai-assistant` | 4K tokens | Session memory | Low-Medium |
| **Data ingestion** | `webhook-to-database` | Standard | Basic | Low |

#### **Q: What are the prerequisites?**

| Component | Required For | How to Set Up |
|-----------|-------------|---------------|
| **n8n instance** | Deployment (`--deploy`) | Must be running at `http://localhost:5678` |
| **n8n API key** | Deployment | Already configured in `config.json` |
| **Telegram credentials** | `telegram-ai-assistant` | Create via n8n UI (instructions provided) |
| **Database credentials** | `webhook-to-database` | Set up via n8n credentials manager |
| **Ollama/AI services** | AI-powered workflows | Already configured for localhost |

#### **Q: What happens when I run the command?**

| Phase | Action | Output | Duration |
|-------|--------|--------|----------|
| **Analysis** | Fetch n8n best practices, discover credentials | `🔄 Generating [pattern] with latest best practices` | 1-2 seconds |
| **Context Engineering** | Apply memory optimization, prompt engineering | `🔄 Context optimization: [strategy] memory, [size] tokens` | 1 second |
| **Generation** | Create workflow JSON with context engineering | `✅ Workflow saved: generated-[pattern]-[timestamp].json` | 1 second |
| **Deployment** (if `--deploy`) | Upload to n8n, auto-activate | `✅ Workflow deployed! ID: [id]` / `✅ Workflow activated!` | 3-5 seconds |

#### **Q: What if something goes wrong?**

| Error Type | Typical Message | Solution |
|------------|----------------|----------|
| **Missing credentials** | `❌ No Telegram API credentials found` | Follow provided 5-step setup instructions |
| **n8n not running** | `❌ Deployment failed: Connection refused` | Start n8n: `n8n start` |
| **Invalid API key** | `❌ Deployment failed: 401 Unauthorized` | Check `config.json` API key |
| **Pattern not found** | `⚠️ AI agent patterns not available` | Fixed in recent updates - should work now |

#### **Q: How do I know it's working?**

| Success Indicator | Location | What to Check |
|-------------------|----------|---------------|
| **Local generation** | Generated JSON file | File exists with workflow nodes and connections |
| **Context engineering** | Terminal output | Shows context optimization details |
| **n8n deployment** | n8n interface | Workflow appears in workflows list, status = Active |
| **Functionality** | n8n workflow execution | Manual trigger works, produces expected outputs |

#### **Q: Can I customize the workflows?**

| Customization | Method | Example |
|---------------|--------|---------|
| **Data source** | Use parameters | `--source=api --target=postgres` |
| **AI model** | Specify model | `--ai=ollama` or `--ai=openai` |
| **Schedule** | Set frequency | `--frequency=daily` |
| **Action type** | Define action | `--action=backup` |
| **Manual editing** | Edit generated JSON | Modify before `--deploy` |

---

### 🔧 System Architecture

```
┌─ Claude CLI ────────────┐    ┌─ n8n Instance ──────┐    ┌─ Local Services ────┐
│ ./generate command      │    │ Workflow execution  │    │ Ollama (LLM)        │
│ Context engineering     │──→ │ Credential storage  │ ←─→│ Whisper (Speech)    │
│ Pattern generation      │    │ API endpoints       │    │ Local databases     │
│ Auto-deployment        │    │ UI management       │    │ External APIs       │
└────────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### 📊 Context Engineering Features

| Feature | Single Agent | Chained Requests | Multi-Agent Gatekeeper | Multi-Agent Teams |
|---------|-------------|------------------|----------------------|------------------|
| **Context Window** | 4,000 tokens | 3,000 tokens | 6,000 tokens | 8,000 tokens |
| **Memory Strategy** | Persistent session | Pipeline memory | Distributed shared | Collaborative memory |
| **Compression Threshold** | 70% | 70% | 60% | 50% |
| **Prompt Engineering** | Role-focused | Stage-focused | Coordination-focused | Collaboration-focused |
| **Quality Evaluation** | ✅ RAGAS-style | ✅ RAGAS-style | ✅ RAGAS-style | ✅ RAGAS-style |

---

### 🎯 Next Steps After Generation

1. **Review Generated Workflow**: Check the JSON file for correctness
2. **Test Locally**: Import into n8n manually if needed
3. **Deploy**: Use `--deploy` flag for automatic deployment
4. **Configure Credentials**: Set up any missing external service credentials
5. **Activate & Test**: Trigger the workflow to verify functionality
6. **Monitor**: Check n8n execution logs for performance

---

**💡 Pro Tip**: Always start with `./generate --list-patterns` to see current capabilities, then use the pattern that best matches your use case complexity requirements.