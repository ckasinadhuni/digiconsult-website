# System Dependencies Analysis

## Current Infrastructure Stack

### Core Services
| Service | Container | Image | Purpose | Update Strategy |
|---------|-----------|--------|---------|-----------------|
| **n8n** | n8n | n8nio/n8n:latest | Workflow automation engine | Docker image updates |
| **Ollama** | ollama | ollama/ollama:latest | Local LLM (mistral:7b) | Docker + model updates |
| **Qdrant** | qdrant | qdrant/qdrant:v1.7.3 | Vector database | Docker image updates |
| **Faster-Whisper** | faster-whisper-small | local/faster-whisper:latest | Speech-to-text service | Local build updates |
| **Caddy** | caddy | caddy:latest | Reverse proxy + SSL | Docker image updates |

### Network Architecture
- **External Network:** `n8n_net` - Connects all services
- **SSL Termination:** Caddy handles HTTPS for all services
- **Service URLs:**
  - n8n: https://n8n.digiconsult.ca
  - Ollama: https://ollama.digiconsult.ca  
  - Qdrant: https://qdrant.digiconsult.ca
  - Faster-Whisper: https://fasterwhisper.digiconsult.ca

### Data Persistence
| Volume | Purpose | Critical Level | Backup Priority |
|--------|---------|----------------|-----------------|
| `n8n_n8n_data` | Workflows, credentials, executions | **CRITICAL** | 🔴 Daily |
| `ollama_data` | LLM models (~4GB mistral:7b) | High | 🟡 Weekly |
| `qdrant_data` | Vector embeddings | Medium | 🟡 Weekly |
| `fasterwhisper_cache` | Model cache | Low | 🟢 Monthly |
| `caddy_data` | SSL certificates | High | 🟡 Weekly |

### Version Dependencies
- **Docker Engine:** 27.5.1 (ARM64)
- **Docker Compose:** 1.29.2 (Legacy - compatibility issues noted)
- **n8n:** 1.107.3 (Official latest)
- **Node.js Runtime:** Built into n8n container
- **Python:** Host system for automation scripts

## Update Impact Matrix

### Low Risk (Automated Safe)
- ✅ **Caddy** - Proxy updates don't affect data
- ✅ **Faster-Whisper** - Model cache rebuilds automatically

### Medium Risk (Require Testing)  
- ⚠️ **Ollama** - Model compatibility across versions
- ⚠️ **Qdrant** - Database migration considerations

### High Risk (Require Backup + Validation)
- 🔴 **n8n** - Workflow compatibility, API changes
- 🔴 **Docker Engine** - Container runtime changes

## Automated Update Strategy

### Daily Monitoring
- Health checks for all services
- Version drift detection
- API accessibility validation
- Workflow execution testing

### Weekly Updates (Low Risk)
- Caddy proxy updates
- Security patches for base images
- Cache cleanups

### Bi-weekly Updates (Medium Risk)
- Ollama model updates
- Qdrant version updates  
- Performance optimizations

### Monthly Updates (High Risk)
- n8n major version updates
- Docker engine updates
- System-level changes

## Dependency Chain Analysis

```
Internet → Caddy → n8n ← Ollama
                 ↓
              Qdrant
                 ↓
          Faster-Whisper
```

### Critical Path
1. **Caddy Failure** → All services offline
2. **n8n Failure** → Workflow automation stops
3. **Ollama Failure** → AI responses fail
4. **Qdrant Failure** → Vector search unavailable
5. **Faster-Whisper Failure** → Voice processing fails

### Resilience Measures
- **Service Health Monitoring** → Automatic restart policies
- **Data Backup Strategy** → Volume snapshots before updates  
- **Rollback Capability** → Previous image versions retained
- **Alternative Paths** → Direct API access for critical functions

## Automation Requirements

### Pre-Update Validation
1. Service health checks
2. Data backup verification
3. Version compatibility testing
4. Dependency chain validation

### Update Process
1. Stop non-critical services first
2. Update with data preservation
3. Validate functionality
4. Rollback on failure

### Post-Update Verification
1. All services responding
2. API endpoints accessible
3. Workflows executable
4. Data integrity confirmed

This analysis forms the foundation for the 7-day automated update system design.