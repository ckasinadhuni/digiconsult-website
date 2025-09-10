# DigiConsult.ca Authentication System Documentation

## Overview
Complete Authelia-based authentication system integrated with the main DigiConsult website, providing elegant single sign-on across all services with selective protection and sophisticated user experience.

## System Architecture

### Core Components
1. **Authelia Authentication Service** - Central authentication provider
2. **Caddy Reverse Proxy** - SSL termination and forward authentication
3. **Main Website** - Integrated authentication UI with login/logout functionality
4. **Admin UI** - User management interface for administrators

### Authentication Flow
1. User visits main website (https://digiconsult.ca)
2. JavaScript detects authentication status via API endpoints
3. Shows login button (unauthenticated) or user initials (authenticated)
4. Login redirects to Authelia portal (https://auth.digiconsult.ca)
5. After authentication, user returns to main site with active session
6. Session provides automatic access to all authorized subdomains

## Repository Structure

### Git Repositories
```
/home/ubuntu/website/          - Main website with authentication integration
/home/ubuntu/n8n/             - Authelia configuration and services  
/home/ubuntu/caddy/           - Reverse proxy configuration
```

### Configuration Files
```
/home/ubuntu/website/
├── index.html                 - Main website with auth UI integration
├── style-elegant.css          - Authentication styling (elegant design)
└── script-elegant.js          - Authentication JavaScript functionality

/home/ubuntu/n8n/
├── docker-compose.yml         - All services configuration
├── authelia/
│   ├── configuration.yml      - Authelia main configuration
│   ├── users_database.yml     - User database (3 users)
│   └── db.sqlite3            - Session storage
└── authelia-admin/
    ├── server.js             - Admin UI Node.js application
    ├── views/                - EJS templates for admin interface
    └── Dockerfile            - Admin UI container configuration

/home/ubuntu/caddy/
├── Caddyfile                 - Reverse proxy rules and SSL
└── docker-compose.yml        - Caddy container configuration
```

## User Management

### Current Users
| Username   | Email                    | Groups                | Access Level        |
|------------|--------------------------|----------------------|---------------------|
| ck         | ck@digiconsult.ca       | admins, users        | Full access (2FA)   |
| tejamarthy | tejamarthy@digiconsult.ca| developers, users    | Developer access    |
| info       | info@digiconsult.ca     | analysts, users      | Limited access      |

### Access Control Rules
| Domain | Policy | Required Groups | Description |
|--------|--------|-----------------|-------------|
| digiconsult.ca | bypass | - | Main site with integrated auth |
| n8n.digiconsult.ca | bypass | - | Has own authentication |
| auth.digiconsult.ca | - | - | Authentication portal |
| admin.digiconsult.ca | two_factor | admins | Admin UI (2FA required) |
| postgresql.digiconsult.ca | two_factor | admins | Database admin (2FA) |
| ollama.digiconsult.ca | one_factor | admins, developers | AI chat interface |
| qdrant.digiconsult.ca | one_factor | admins, analysts | Vector database |
| faster-whisper.digiconsult.ca | one_factor | users | Speech-to-text API |

## Service Configuration

### Docker Services
```yaml
# All services run in n8n_net network
services:
  authelia:          # Authentication service (port 9091)
  authelia-admin:    # Admin UI (port 3001)
  caddy:             # Reverse proxy (ports 80, 443)
  n8n:               # Workflow automation (port 5678)  
  postgres:          # Database (port 5432)
  ollama:            # AI models (port 11434)
  open-webui:        # Chat interface (port 3000)
  qdrant:            # Vector DB (port 6333)
  faster-whisper:    # Speech API (port 8000)
  adminer:           # DB admin (port 8080)
```

### SSL Certificates
- Automatic Let's Encrypt certificates for all domains
- HTTP/3 support enabled
- Security headers configured (HSTS, CSP, etc.)

## Website Integration Features

### Authentication UI
- **Login Button**: Elegant integration matching site design
- **User Profile**: Circular initials display (e.g., "CK" for ck@digiconsult.ca)
- **User Menu**: Dropdown with user info and logout option
- **Responsive Design**: Mobile-optimized authentication interface

### JavaScript Functionality
- Automatic authentication status detection
- Periodic session checks (every 5 minutes)
- Elegant loading states and transitions
- User initials generation from email addresses
- Session management and logout handling

### CSS Design Integration
- Uses site's sophisticated color palette (brand red: #E53E3E)
- Maintains elegant typography and spacing system
- Professional hover effects and animations
- Consistent with enterprise consulting aesthetic

## API Endpoints

### Authentication APIs
```
GET /api/auth/check    - Returns "OK" if authenticated
GET /api/auth/user     - Returns user info JSON:
{
  "email": "user@domain.com",
  "displayName": "Display Name", 
  "groups": "group1,group2"
}
```

## Security Features

### Authentication
- File-based user database with PBKDF2 password hashing
- Two-factor authentication for admin access
- Session management with 4-hour expiration, 30-minute inactivity
- Rate limiting: 5 failed attempts, 5-minute lockout

### Network Security
- All traffic encrypted with TLS 1.3
- Strict Transport Security (HSTS) enabled
- Content Security Policy (CSP) headers
- Cross-frame protection (X-Frame-Options: DENY)

## Operational Commands

### Service Management
```bash
# Restart authentication service
cd /home/ubuntu/n8n && docker-compose restart authelia

# Restart reverse proxy  
cd /home/ubuntu/caddy && docker-compose restart caddy

# View authentication logs
docker logs authelia --tail 50

# Check service status
docker-compose ps
```

### User Management
```bash
# Access admin UI
https://admin.digiconsult.ca

# Generate new password hash (for manual user creation)
docker exec -it authelia authelia hash-password 'newpassword'
```

### Git Operations
```bash
# Update website authentication code
cd /home/ubuntu/website && git add . && git commit -m "description"

# Update system configuration
cd /home/ubuntu/n8n && git add . && git commit -m "description"

# Update proxy configuration  
cd /home/ubuntu/caddy && git add . && git commit -m "description"
```

## Troubleshooting

### Common Issues
1. **Login button not appearing**: Check authentication API endpoints
2. **Redirect loops**: Verify Authelia access control rules
3. **SSL certificate issues**: Check DNS propagation and Caddy logs
4. **User info not displaying**: Verify Caddy header forwarding

### Log Locations
```bash
docker logs authelia      # Authentication service logs
docker logs caddy         # Reverse proxy logs  
docker logs authelia-admin # Admin UI logs
```

## Future Enhancements
- Integration with external identity providers (LDAP, SAML)
- Enhanced user profile management
- Audit logging and monitoring
- API key management for service access
- Mobile app authentication support

---

**Last Updated**: 2025-08-29  
**Version**: 1.0.0  
**Contact**: ck@digiconsult.ca