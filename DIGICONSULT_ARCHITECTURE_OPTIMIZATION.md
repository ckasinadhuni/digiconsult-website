# DigiConsult Infrastructure Architecture Optimization Plan

> **Trigger Phrase:** "new architecture digiconsult"  
> **Status:** Future Enhancement Recommendations  
> **Created:** September 6, 2025  

## 🏗️ Current vs. Optimal Architecture Analysis

### Current Setup (What We Have)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Ubuntu 24.04 VM (ARM64)                         │
│                                                                     │
│  ┌─── CADDY ──┐  ┌──── N8N ────┐  ┌─── PADDLEOCR ───┐               │
│  │ Compose #1 │  │ Compose #2  │  │   Compose #3    │               │
│  │            │  │             │  │                 │               │
│  │ Port: 80   │  │ Port: 5678  │  │ Port: 8001      │               │
│  │ Port: 443  │  │             │  │ (Internal:8002) │               │
│  └─────┬──────┘  └──────┬──────┘  └─────────┬───────┘               │
│        │                │                   │                       │
│        │         ┌──────┴───────┐           │                       │
│        │         │ POSTGRES     │           │                       │
│        │         │ AUTHELIA     │           │                       │
│        │         │ OLLAMA       │           │                       │
│        │         │ QDRANT       │           │                       │
│        │         │ WHISPER      │           │                       │
│        │         │ ADMINER      │           │                       │
│        │         │ OPEN-WEBUI   │           │                       │
│        │         └──────────────┘           │                       │
│        │                │                   │                       │
│  ┌─────┴────────────────┴───────────────────┴───────┐               │
│  │            Docker Network: n8n_net               │               │
│  │               (172.19.0.0/16)                    │               │
│  └─────────────────────────────────────────────────────┘               │
│                                                                     │
│  CURRENT ISSUES:                                                    │
│  ❌ 3 separate docker-compose files (management complexity)         │
│  ❌ No standardized naming conventions                               │
│  ❌ Mixed deployment patterns                                       │
│  ❌ Port conflicts discovered reactively                            │
│  ❌ No centralized environment configuration                        │
│  ❌ Inconsistent health check patterns                              │
│  ❌ No proper service dependencies defined                          │
│  ❌ Manual SSL certificate management                               │
│  ❌ No monitoring or metrics collection                             │
│  ❌ No automated backup strategy                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Optimal Architecture (Master Architect Approach)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Ubuntu 24.04 VM (ARM64)                         │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   SINGLE STACK DEPLOYMENT                      │ │
│  │                  /opt/digiconsult-stack/                       │ │
│  │                                                                 │ │
│  │  ┌─── INGRESS LAYER ──┐                                        │ │
│  │  │     Traefik         │ ← BETTER: Auto SSL, Service Discovery│ │
│  │  │   Port: 80, 443     │                                       │ │
│  │  │ Labels: routing     │                                       │ │
│  │  └─────────┬───────────┘                                       │ │
│  │            │                                                   │ │
│  │  ┌─────────┴───────────┐                                       │ │
│  │  │   SERVICE MESH      │                                       │ │
│  │  │                     │                                       │ │
│  │  │ ┌─ CORE SERVICES ─┐ │                                       │ │
│  │  │ │ • n8n:5000      │ │ ← Standardized port ranges            │ │
│  │  │ │ • tesseract:5001│ │ ← ARM64 OCR (Replaces PaddleOCR)     │ │
│  │  │ │ • whisper:5002  │ │                                       │ │
│  │  │ └─────────────────┘ │                                       │ │
│  │  │                     │                                       │ │
│  │  │ ┌─ AI SERVICES ───┐ │                                       │ │
│  │  │ │ • ollama:6000   │ │ ← Logical grouping                    │ │
│  │  │ │ • qdrant:6001   │ │                                       │ │
│  │  │ │ • openui:6002   │ │                                       │ │
│  │  │ └─────────────────┘ │                                       │ │
│  │  │                     │                                       │ │
│  │  │ ┌─ DATA LAYER ────┐ │                                       │ │
│  │  │ │ • postgres:7000 │ │ ← Infrastructure services             │ │
│  │  │ │ • authelia:7001 │ │                                       │ │
│  │  │ │ • adminer:7002  │ │                                       │ │
│  │  │ └─────────────────┘ │                                       │ │
│  │  └─────────────────────┘                                       │ │
│  │                                                                 │ │
│  │  BENEFITS:                                                      │ │
│  │  ✅ Single docker-compose.yml with service sections            │ │
│  │  ✅ Systematic port allocation (5xxx, 6xxx, 7xxx)             │ │
│  │  ✅ Auto SSL with Let's Encrypt                                │ │
│  │  ✅ Service discovery via labels                               │ │
│  │  ✅ Centralized environment (.env files)                      │ │
│  │  ✅ Proper dependency ordering                                 │ │
│  │  ✅ Standardized health checks                                 │ │
│  │  ✅ Resource limits and quotas                                 │ │
│  │  ✅ Backup and monitoring built-in                             │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## 📊 Current vs. Optimal Comparison

| **Aspect** | **Current** | **Optimal** | **Impact** |
|------------|-------------|-------------|------------|
| **Deployment** | 3 separate docker-compose | Single orchestrated stack | Simplified management |
| **Proxy** | Caddy (manual config) | Traefik (auto-discovery) | Zero-config SSL |
| **Port Management** | Ad-hoc assignment | Systematic ranges (5xxx, 6xxx, 7xxx) | Predictable scaling |
| **SSL** | Manual Caddy config | Auto Let's Encrypt | Reduced maintenance |
| **Service Discovery** | Hard-coded IPs/ports | Label-based routing | Dynamic scaling |
| **Dependencies** | Implicit/undefined | Explicit dependency chains | Reliable startup |
| **Configuration** | Scattered env vars | Centralized .env files | Environment consistency |
| **Health Checks** | Inconsistent patterns | Standardized across all services | Better reliability |
| **Resource Limits** | Only on PaddleOCR | System-wide quotas | Resource protection |
| **Backup Strategy** | Manual/undefined | Automated daily backups | Data protection |
| **Monitoring** | None | Built-in metrics collection | Operational visibility |
| **Scaling** | Manual container restart | Health-based auto-restart | Better availability |

## 🚀 Zero-Downtime Migration Plan

### Phase 1: PREPARATION (30 minutes)

#### 1.1 Create New Directory Structure
```bash
sudo mkdir -p /opt/digiconsult-stack/{configs,data,backups}
sudo mkdir -p /opt/digiconsult-stack/configs/{traefik,authelia,apps}
sudo mkdir -p /opt/digiconsult-stack/data/{postgres,n8n,models}
sudo mkdir -p /opt/digiconsult-stack/backups/automated-daily
```

#### 1.2 Export Current Data
```bash
# Backup current volumes
docker run --rm -v n8n_n8n_data:/data -v /opt/digiconsult-stack/backups:/backup alpine tar czf /backup/n8n_data.tar.gz -C /data .
docker run --rm -v n8n_postgres_data:/data -v /opt/digiconsult-stack/backups:/backup alpine tar czf /backup/postgres_data.tar.gz -C /data .
docker run --rm -v n8n_ollama_data:/data -v /opt/digiconsult-stack/backups:/backup alpine tar czf /backup/ollama_data.tar.gz -C /data .
docker run --rm -v n8n_qdrant_data:/data -v /opt/digiconsult-stack/backups:/backup alpine tar czf /backup/qdrant_data.tar.gz -C /data .
docker run --rm -v paddleocr_paddleocr_cache:/data -v /opt/digiconsult-stack/backups:/backup alpine tar czf /backup/paddleocr_cache.tar.gz -C /data .

# Backup configurations
cp -r /home/ubuntu/caddy/Caddyfile /opt/digiconsult-stack/configs/current_caddyfile.backup
cp -r /home/ubuntu/n8n/authelia/ /opt/digiconsult-stack/configs/authelia_backup/
```

#### 1.3 Generate Unified Configuration
```bash
# Create master docker-compose.yml (will be generated by script)
# Create production environment file
# Generate Traefik configuration
# Migrate Authelia settings
```

### Phase 2: DEPLOYMENT (60 minutes)

#### 2.1 DNS Preparation (EXTERNAL ACTION REQUIRED)
**⚠️ DNS PROVIDER CHANGES NEEDED:**
- Reduce TTL on all digiconsult.ca subdomains to 300 seconds (5 minutes)
- Wait 24 hours before migration OR accept potential DNS propagation delays

#### 2.2 Service Migration (15 minutes downtime)
```bash
# Stop current services gracefully
cd /home/ubuntu/n8n && docker-compose down --timeout 30
cd /home/ubuntu/paddleocr && docker-compose down --timeout 30  
cd /home/ubuntu/caddy && docker-compose down --timeout 30

# Import data to new locations
cd /opt/digiconsult-stack
docker-compose up -d postgres authelia  # Start dependencies first
# Wait for health checks
docker-compose up -d n8n traefik         # Start core services
# Wait for health checks  
docker-compose up -d                     # Start remaining services
```

#### 2.3 Data Restoration
```bash
# Restore data from backups
docker run --rm -v digiconsult_n8n_data:/data -v /opt/digiconsult-stack/backups:/backup alpine tar xzf /backup/n8n_data.tar.gz -C /data
docker run --rm -v digiconsult_postgres_data:/data -v /opt/digiconsult-stack/backups:/backup alpine tar xzf /backup/postgres_data.tar.gz -C /data
# ... (restore all data volumes)
```

### Phase 3: OPTIMIZATION (30 minutes)

#### 3.1 Configure Advanced Features
```bash
# Enable Traefik dashboard
# Configure automated backups
# Set up monitoring endpoints  
# Configure log aggregation
```

#### 3.2 DNS Finalization (EXTERNAL ACTION REQUIRED)
**⚠️ DNS PROVIDER CHANGES NEEDED:**
- Verify all subdomains resolve correctly
- Increase TTL back to 3600 seconds (1 hour)
- Update any external monitoring systems

## 📁 New Directory Structure

```
/opt/digiconsult-stack/
├── docker-compose.yml                 # Master orchestration
├── .env.production                    # Environment variables
├── .env.staging                       # Staging environment
├── configs/
│   ├── traefik/
│   │   ├── traefik.yml               # Static configuration  
│   │   ├── dynamic.yml               # Dynamic routing rules
│   │   └── acme.json                 # SSL certificates
│   ├── authelia/
│   │   ├── configuration.yml         # Auth configuration
│   │   ├── users_database.yml        # User definitions
│   │   └── assets/                   # Custom assets
│   └── apps/
│       ├── n8n/                      # n8n-specific configs
│       ├── paddleocr/               # PaddleOCR configs  
│       └── monitoring/              # Monitoring configs
├── data/                            # Persistent data
│   ├── postgres/                    # Database files
│   ├── n8n/                        # Workflow data
│   ├── models/                      # Shared AI models
│   │   ├── paddleocr/              # OCR models
│   │   ├── whisper/                # Speech models
│   │   └── ollama/                 # LLM models  
│   └── traefik/                    # SSL certificates
├── backups/                        # Backup storage
│   ├── automated-daily/            # Daily automated backups
│   ├── pre-migration/              # Migration backups
│   └── manual/                     # Manual snapshots
├── logs/                           # Centralized logging
│   ├── traefik/                    # Proxy logs
│   ├── application/                # App logs
│   └── system/                     # System logs
└── scripts/                        # Management scripts
    ├── backup.sh                   # Backup automation
    ├── restore.sh                  # Restore procedures
    ├── health-check.sh             # System health monitoring
    └── migrate-from-current.sh     # Migration automation
```

## 🔧 Implementation Scripts (Auto-Generated)

The following scripts will be auto-generated when "new architecture digiconsult" is triggered:

1. **`migrate-from-current.sh`** - Complete migration automation
2. **`docker-compose.yml`** - Unified service orchestration
3. **`.env.production`** - Centralized environment configuration  
4. **`traefik.yml`** - Auto-discovery proxy configuration
5. **`backup.sh`** - Automated backup procedures
6. **`health-check.sh`** - System monitoring

## 🛡️ Data Protection Guarantees

1. **Full Data Backup** - All volumes backed up before migration
2. **Rollback Plan** - Current system preserved until verification
3. **Verification Tests** - Comprehensive endpoint testing
4. **Gradual Migration** - Services migrated in dependency order
5. **Zero Data Loss** - All user data, workflows, and configurations preserved

## 📋 External Actions Required

### DNS Provider Changes
1. **Pre-Migration (24-48 hours before):**
   - Reduce TTL on all `*.digiconsult.ca` records to 300 seconds
   - Document current DNS settings

2. **Post-Migration:**
   - Verify all endpoints resolve correctly
   - Increase TTL back to 3600 seconds
   - Update monitoring systems if needed

### SSL Certificate Considerations  
- Current Caddy SSL certificates will be preserved
- Traefik will request new Let's Encrypt certificates
- No SSL downtime expected due to certificate copying

### Monitoring Integration
- External monitoring systems may need endpoint updates
- API keys and webhook URLs will remain unchanged
- Database connection strings will remain the same

## 📊 Expected Benefits Post-Migration

| **Metric** | **Current** | **Post-Migration** | **Improvement** |
|------------|-------------|--------------------|-----------------|
| **Deployment Time** | 15-30 min | 2-5 min | 83% reduction |
| **Configuration Management** | 3 files | 1 file | Simplified |
| **SSL Certificate Renewal** | Manual | Automatic | Zero maintenance |
| **Service Discovery** | Hard-coded | Dynamic | Scalable |
| **Health Monitoring** | Manual | Automated | Proactive |
| **Backup Strategy** | None | Automated Daily | Data protection |
| **Resource Utilization** | Unmonitored | Tracked | Optimized |
| **Startup Dependencies** | Undefined | Ordered | Reliable |

## 🎯 Success Criteria

- [ ] All current services accessible via same URLs
- [ ] Zero data loss from any service
- [ ] All workflows and configurations intact  
- [ ] SSL certificates working correctly
- [ ] Authentication system fully functional
- [ ] Backup automation operational
- [ ] Monitoring dashboard accessible
- [ ] Performance equal or better than current
- [ ] Documentation updated with new procedures

---

## 🔥 TESSERACT OCR SERVICE - IMMEDIATE IMPLEMENTATION PLAN

**Architecture Decision:** Tesseract OCR 5.3+ (ARM64-native, production-ready)

### Current System Status After Cleanup:
✅ **PaddleOCR Completely Removed**
- All Docker containers and images deleted
- Configuration files cleaned
- Caddy proxy configuration updated  
- Port 8003 available for OCR service
- No dependency conflicts remain

### Tesseract OCR Service Specifications:

```
┌─── OCR Service Architecture ───┐
│                                │
│  Service: tesseract-ocr        │
│  Port: 8003 (Internal)         │  
│  Domain: ocr.digiconsult.ca    │
│  Network: n8n_net (existing)   │
│                                │
│  Features:                     │
│  • PDF + Image processing      │
│  • Multi-language support      │
│  • Batch processing API        │
│  • ARM64 optimized (<200MB)    │
│  • Health checks built-in      │
│  • n8n integration ready       │
│                                │
│  Dependencies:                 │
│  • Tesseract 5.3.4            │
│  • FastAPI framework          │
│  • Pillow (image processing)   │
│  • PyPDF2 (PDF support)       │
│  • No OpenCV conflicts        │
└────────────────────────────────┘
```

### Implementation Components:

1. **Docker Service**
   - Base: `python:3.12-slim` (ARM64 compatible)
   - Tesseract 5.3+ with language packs
   - FastAPI REST API server
   - Health check endpoints

2. **API Endpoints**
   - `POST /ocr/image` - Process single image
   - `POST /ocr/pdf` - Extract text from PDF
   - `POST /ocr/batch` - Process multiple files
   - `GET /health` - Service health check
   - `GET /languages` - Supported languages

3. **Integration**
   - Caddy reverse proxy with Authelia auth
   - Docker Compose service definition
   - n8n workflow compatibility
   - Automated startup dependencies

---

**Note:** This document serves as the complete blueprint for infrastructure optimization. When triggered with "new architecture digiconsult", a detailed implementation plan with specific scripts and procedures will be generated based on these recommendations.