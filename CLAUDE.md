# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a comprehensive DigiConsult.ca AI-powered business platform built on a microservices architecture with Docker containers. The system integrates multiple services including workflow automation (n8n), authentication, AI services, and document processing.

### Core Services

**n8n Workflow Platform** (`/n8n/`): 
- Primary automation engine with PostgreSQL backend
- Main deployment: `docker-compose.yml` in `/n8n/`
- Access via `n8n.digiconsult.ca`

**Authentication Layer**:
- **Authelia** (`/n8n/authelia/`): Primary SSO authentication service
- **PocketBase** (`/pocketbase-auth/`): Secondary auth service for specific use cases
- **Auth Service** (`/auth-service/`): Node.js-based authentication middleware

**AI/ML Services**:
- **Ollama**: Local AI model server (port 11434)
- **Qdrant**: Vector database (port 6333) 
- **Faster-Whisper**: Speech-to-text service (port 8000)
- **Tesseract OCR**: Document processing (port 8003)

**Infrastructure**:
- **Caddy** (`/caddy/`): Reverse proxy with SSL termination and forward auth
- **PostgreSQL**: Primary database for n8n and auth services
- **Website** (`/website/`): Main DigiConsult.ca frontend

### Special Projects

**Zatuka** (`/zatuka/`): Tax office voice assistant POC with Spanish/American user support, uses PocketBase for data persistence and Prisma for database management.

## Development Commands

### Docker Operations
```bash
# Start all services
cd /home/ubuntu/n8n && docker-compose up -d

# Stop all services  
cd /home/ubuntu/n8n && docker-compose down

# View logs
cd /home/ubuntu/n8n && docker-compose logs -f [service-name]

# Restart specific service
cd /home/ubuntu/n8n && docker-compose restart [service-name]

# Start PocketBase auth service
cd /home/ubuntu/pocketbase-auth && docker-compose up -d

# Start Caddy proxy
cd /home/ubuntu/caddy && docker-compose up -d
```

### Database Management
```bash
# PostgreSQL access via Adminer
# Visit: postgresql.digiconsult.ca (auth required)

# PGAdmin4 access
# Visit: http://localhost:8081
# Credentials: admin@digiconsult.ca / DigiConsult2025!

# PocketBase admin
# Visit: auth2.digiconsult.ca/_/ (port 8091)
```

### Auth Service Development
```bash
cd /home/ubuntu/auth-service
npm install
npm run dev     # Development mode with nodemon
npm test        # Run Jest tests
npm run lint    # ESLint checks
npm run migrate # Database migrations
```

### Zatuka Development
```bash
cd /home/ubuntu/zatuka
npm install
npx prisma generate  # Generate Prisma client
npx prisma db push   # Push schema to database
```

## Network Architecture

All services run on the `n8n_net` external Docker network. Key access points:

- **Main Site**: https://digiconsult.ca 
- **Authentication**: https://auth.digiconsult.ca
- **n8n Platform**: https://n8n.digiconsult.ca
- **PocketBase**: https://auth2.digiconsult.ca
- **AI Chat**: https://ollama.digiconsult.ca
- **Voice Processing**: https://whisper.digiconsult.ca (auth required)
- **OCR Service**: https://ocr.digiconsult.ca (trial+ users)

## File Structure Patterns

**Docker Configurations**: Each service has its own `docker-compose.yml` and related configs
**Backup Systems**: Multiple backup directories with timestamps (e.g., `migration-safety-backup-*`)
**Claude Prompts**: Development automation tools in `/claude-prompts/`
**Shared Documentation**: Centralized docs in `/shared-docs/` accessible via admin portal

## Authentication Flow

The system uses Authelia-based forward authentication with Caddy:
1. Caddy intercepts protected routes
2. Forward auth check to Authelia (port 9091)
3. Unauthenticated users redirected to auth.digiconsult.ca
4. Session provides access to authorized subdomains
5. Different permission levels: public, trial+, analysts, admins

## Environment Configuration

Key environment files:
- `/n8n/.env`: n8n configuration including N8N_PORT, database settings
- `/n8n/authelia/configuration.yml`: Authentication rules and user permissions
- `/pocketbase-auth/data/`: PocketBase database and storage

## Development Notes

- Use absolute paths when referencing files across services
- All services communicate via internal Docker network names
- Database migrations are handled per-service (n8n uses built-in, PocketBase uses migrations folder)
- Backup workflows include both data and configuration preservation
- The system supports parallel authentication systems (Authelia + PocketBase) for different use cases