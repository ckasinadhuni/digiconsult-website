# Docker Version Compatibility Learnings

## Issue Encountered
**Date:** 2025-01-20  
**Problem:** docker-compose 1.29.2 incompatible with Docker 27.5.1  
**Error:** `KeyError: 'ContainerConfig'` in `get_container_data_volumes()`

## Root Cause Analysis
1. **Version Mismatch:** Legacy docker-compose (1.29.2) cannot read metadata from modern Docker images
2. **Image Transition:** Custom `n8n-arm64` to official `n8nio/n8n:latest` caused container metadata conflicts
3. **Compose Version:** No modern `docker compose` plugin available

## Solution Applied
1. **Clean State Approach:** Removed old containers completely before switching images
2. **Direct Docker Commands:** Bypassed docker-compose for container creation
3. **Volume Preservation:** Maintained data integrity using persistent volumes

```bash
# Working solution:
docker stop old_container && docker rm old_container
docker run -d --name n8n \
  --restart unless-stopped \
  --env-file .env \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  --network n8n_net \
  n8nio/n8n:latest
```

## Key Learnings
### ✅ Safe Practices
- **Always validate compatibility** before image transitions
- **Clean container state** when switching between custom/official images
- **Preserve data volumes** - they're separate from container metadata issues
- **Use direct Docker commands** when compose fails due to version conflicts

### ⚠️ Warning Signs
- `KeyError: 'ContainerConfig'` = Version compatibility issue
- Docker Compose failing on image metadata = Outdated compose version
- Container recreation failures = Image metadata conflicts

### 🔧 Prevention
- **Regular Updates:** Keep docker-compose in sync with Docker engine
- **Version Monitoring:** Check compatibility before major image switches
- **Testing Strategy:** Validate on non-production first
- **Backup Strategy:** Always backup volumes before container changes

## Future Automation Requirements
1. **Version Compatibility Check:** Auto-validate docker/compose versions
2. **Safe Update Process:** Automated container recreation with data preservation
3. **Rollback Strategy:** Quick revert to previous working state
4. **Monitoring:** Alert on version drift between Docker components

## Impact Assessment
- **Data Loss:** ❌ None - volumes preserved correctly
- **Downtime:** ⏱️ ~10 minutes for troubleshooting and recreation  
- **Functionality:** ✅ All features maintained after update
- **Performance:** ✅ No degradation, actually improved with official image

## Validation Success
- **n8n Version:** Successfully updated from 1.106.3 → 1.107.3
- **API Access:** ✅ Working with new API key
- **Workflows:** ✅ 6 workflows preserved
- **Credentials:** ✅ All credentials intact
- **Node Types:** ✅ Standard nodes functional (LangChain requires ai-beta image)

This experience reinforces the importance of version compatibility validation in Docker environments and the value of persistent volume strategies for data protection.