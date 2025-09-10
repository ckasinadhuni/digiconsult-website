# System Setup Documentation

## Current Infrastructure Overview

### Active Docker Containers
- **n8n** (n8nio/n8n:latest) - Workflow automation platform
- **ollama** (ollama/ollama:latest) - Local AI model server
- **qdrant** (qdrant/qdrant:v1.7.3) - Vector database
- **faster-whisper-small** (local/faster-whisper:latest) - Speech-to-text service
- **caddy** (caddy:latest) - Web server/reverse proxy

### Network Architecture
- **Primary Network**: `n8n_net` (bridge network)
- All services communicate via this internal network
- External access via port mappings:
  - n8n: :5678
  - ollama: :11434  
  - qdrant: :6333
  - faster-whisper: :8000
  - caddy: :80, :443

### Data Persistence
- **n8n_data**: /home/node/.n8n (contains database.sqlite, workflows, configs)
- **ollama_data**: /root/.ollama (AI models)
- **qdrant_data**: /qdrant/storage (vector database)
- **fasterwhisper_cache**: /root/.cache (speech models)

### Current Database Setup
- **n8n Database**: SQLite (`database.sqlite` - 487KB)
- Located at: `/home/ubuntu/n8n/n8n_data/database.sqlite`

### Key Configuration Files
- **Main compose**: `/home/ubuntu/n8n/docker-compose.yml`
- **Environment**: `/home/ubuntu/n8n/.env`
- **Domain**: n8n.digiconsult.ca (HTTPS enabled)
- **Auth**: Basic auth enabled (admin/SuperSecret123)

### Infrastructure Directories
```
/home/ubuntu/
├── n8n/                          # Active n8n deployment
│   ├── docker-compose.yml        # Main compose file
│   ├── .env                      # Environment config
│   ├── n8n_data/                # Persistent data
│   │   ├── database.sqlite       # Current SQLite DB
│   │   ├── binaryData/
│   │   └── config
│   └── stt-fasterwhisper/       # Custom whisper service
├── digiconsult-infrastructure/   # Alternative/backup infrastructure
├── caddy/                       # Caddy reverse proxy config
└── infra-backups/              # System backups
```

## Services Status
- **n8n**: ✅ Running (Up 9 days)
- **ollama**: ✅ Running (Up 11 days)  
- **qdrant**: ✅ Running (Up 11 days)
- **faster-whisper**: ✅ Running (Up 11 days)
- **caddy**: ✅ Running (Up 9 days)

## Current Limitations
1. **Database**: Using SQLite (single-user, file-based)
2. **No PostgreSQL**: Missing multi-user database capability
3. **Network**: Services already integrated via n8n_net
4. **Security**: Basic auth only, no advanced database security

## Proposed PostgreSQL Integration Plan
1. Add PostgreSQL service to existing docker-compose.yml
2. Configure n8n to use PostgreSQL instead of SQLite
3. Migrate existing SQLite data to PostgreSQL
4. Update networking and security configurations
5. Implement backup strategies for PostgreSQL data

## PostgreSQL Integration Setup Complete

### New PostgreSQL Service Added
- **Image**: postgres:15-alpine
- **Container**: n8n-postgres
- **Database**: n8n (dedicated for n8n data)
- **Schema**: n8n_data (isolated n8n tables)
- **Port**: 5432 (accessible externally)

### Database Users Created
1. **n8n_user**: Full access to n8n_data schema (primary n8n user)
2. **readonly_user**: Read-only access (Password: readonly_secure_pass_2024)
3. **app_user**: Limited write access (Password: app_secure_pass_2024)
4. **metrics_user**: System monitoring (Password: metrics_secure_pass_2024)

### Migration Ready
- **SQLite Backup**: `/home/ubuntu/n8n/sqlite-backups/database-backup-20250829-211019.sqlite`
- **Migration Script**: `/home/ubuntu/n8n/migrate-sqlite-to-postgres.sh`
- **Current User**: ck@digiconsult.ca (preserved)

### Test Users for n8n UI
- **tejamarthy@digiconsult.ca** / TejaMarthyn8n2025! (Admin role)
- **info@digiconsult.ca** / Infon8n2025! (Member role)

### n8n User Permission Levels
- **Owner** (ck@digiconsult.ca): Full system access, manage all workflows/users/settings
- **Admin** (tejamarthy@): Create/edit workflows, manage users, view system settings  
- **Member** (info@): Create/edit own workflows, execute workflows
- **Database Users**: Separate PostgreSQL access for external applications

### Ready to Deploy
Run: `cd /home/ubuntu/n8n && ./migrate-sqlite-to-postgres.sh`

## Web Interfaces Added

### New Services Deployed
- **Open WebUI**: Ollama chat interface (port 3000)
- **Adminer**: PostgreSQL web admin (port 8080)

### Web Access URLs
- **n8n**: https://n8n.digiconsult.ca
- **Ollama Chat**: https://ollama.digiconsult.ca
- **PostgreSQL Admin**: https://postgresql.digiconsult.ca
- **Faster-Whisper API**: https://faster-whisper.digiconsult.ca
- **Qdrant Dashboard**: https://qdrant.digiconsult.ca/dashboard

### Authentication Details
- **Ollama**: No auth required (direct access)
- **PostgreSQL**: Use database credentials (n8n_user, readonly_user, app_user)
- **Faster-Whisper**: No auth required (web UI at /docs endpoint)
- **Qdrant**: No auth required (dashboard access)

## Session Change Log
- **2025-08-29**: Initial system analysis and documentation creation
- **2025-08-29**: PostgreSQL integration complete, migration script ready
- **2025-08-29**: All web interfaces deployed successfully