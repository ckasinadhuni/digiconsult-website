# 🔧 Router Configuration Learnings

## 🚨 **Critical Issues Found:**

### **Initial Problem:**
- Router had only 2 basic conditions: `/search` and `/files`
- Missing multimodal detection for voice, images, documents
- Missing proper connection routing (only 3 outputs instead of 6)
- No fallback for regular text messages

### **Fixed Configuration:**
```json
{
  "options": {"caseSensitive": false, "leftValue": "", "typeValidation": "strict"},
  "conditions": [
    {
      "id": "search_cmd",
      "leftValue": "={{ $json.message.text }}",
      "operator": {"type": "string", "operation": "startsWith", "rightValue": "/search"}
    },
    {
      "id": "files_cmd", 
      "leftValue": "={{ $json.message.text }}",
      "operator": {"type": "string", "operation": "startsWith", "rightValue": "/files"}
    },
    {
      "id": "voice_msg",
      "leftValue": "={{ $json.message.voice }}",
      "operator": {"type": "object", "operation": "exists"}
    },
    {
      "id": "image_msg",
      "leftValue": "={{ $json.message.photo }}",
      "operator": {"type": "array", "operation": "notEmpty"}
    },
    {
      "id": "document_msg",
      "leftValue": "={{ $json.message.document }}",
      "operator": {"type": "object", "operation": "exists"}
    },
    {
      "id": "text_msg",
      "leftValue": "={{ $json.message.text }}",
      "operator": {"type": "string", "operation": "exists"}
    }
  ],
  "combinator": "or"
}
```

### **Connection Fix:**
- Router must have 6 outputs (one per condition)
- Each output routes to appropriate processing node
- All routes can converge to same processor if needed

## 🔑 **Key Learnings for Generator:**

1. **Always validate router conditions count** - should match expected input types
2. **Always verify router output connections** - must equal condition count  
3. **Include multimodal detection patterns** - voice, image, document, text
4. **Test router logic before deployment** - ensure all paths work
5. **Use reliable n8n API patterns** - clean data structure for updates

## 🛠️ **Reliable n8n API Pattern:**
```python
# Get workflow
response = requests.get(f"{base_url}/api/v1/workflows/{id}", headers=headers)

# Update workflow (minimal fields only)
clean_data = {
    "name": workflow["name"],
    "nodes": workflow["nodes"], 
    "connections": workflow["connections"],
    "settings": workflow.get("settings", {})
}
response = requests.put(f"{base_url}/api/v1/workflows/{id}", headers=headers, json=clean_data)
```

## 📋 **Mandatory Router Checklist:**
- [ ] Command detection (/search, /files, etc.)
- [ ] Voice message detection (message.voice exists)
- [ ] Image detection (message.photo not empty)
- [ ] Document detection (message.document exists) 
- [ ] Text fallback (message.text exists)
- [ ] Output count matches condition count
- [ ] All outputs properly connected