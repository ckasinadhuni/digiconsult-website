# 🎯 WORKING n8n WORKFLOW TEMPLATE

**Base Template ID**: `kaVhNfbnkr3tw0j2`
**Name**: 🤖 Fixed AI Agent - From Working Template
**Source**: Cloned from successful manual workflow "My workflow" (wF7FPa9ClbuCAWuI)

## ✅ PROVEN WORKING STRUCTURE

### Node Configuration Standards

#### 1. Telegram Trigger
```json
{
  "type": "n8n-nodes-base.telegramTrigger",
  "typeVersion": 1.2,
  "parameters": {
    "updates": ["message"],
    "additionalFields": {}
  },
  "disabled": false
}
```

#### 2. Switch Node (CRITICAL - Use EXACT Structure)
```json
{
  "type": "n8n-nodes-base.switch", 
  "typeVersion": 3.2,  // MUST be 3.2, not 3
  "parameters": {
    "rules": {
      "values": [
        {
          "conditions": {
            "options": {
              "caseSensitive": true,
              "leftValue": "",
              "typeValidation": "strict",
              "version": 2
            },
            "conditions": [
              {
                "leftValue": "={{ $json.message.voice.file_id }}",
                "rightValue": "",
                "operator": {
                  "type": "string",
                  "operation": "exists", 
                  "singleValue": true
                },
                "id": "unique-uuid-here"
              }
            ],
            "combinator": "and"
          },
          "renameOutput": true,
          "outputKey": "Audio"
        }
        // Additional rules follow same pattern...
      ]
    },
    "options": {}
  },
  "disabled": false
}
```

### Connection Format (EXACT)
```json
{
  "connections": {
    "Telegram Trigger": {
      "main": [
        [{"node": "Switch", "type": "main", "index": 0}]
      ]
    }
  }
}
```

## 🚨 CRITICAL SUCCESS FACTORS

1. **Switch Node Version**: MUST be `typeVersion: 3.2`
2. **Condition Structure**: MUST include `options` with `typeValidation: "strict"`
3. **Unique IDs**: Each condition MUST have unique `id` field
4. **Combinator**: MUST include `combinator: "and"`
5. **Disabled Property**: ALL nodes MUST have `disabled: false`
6. **Connection Format**: Use exact array structure `[[{node, type, index}]]`

## 🎯 TEMPLATE USAGE

**For all future workflows:**
1. Start with this template ID: `kaVhNfbnkr3tw0j2`
2. Clone the structure exactly
3. Add nodes incrementally, testing each step
4. Never use Switch typeVersion 3 - always use 3.2
5. Always include all required properties from this template

## 📋 TESTED WORKING COMPONENTS

- ✅ Telegram Trigger → Switch routing
- ✅ Voice message detection (`$json.message.voice.file_id`)
- ✅ Document detection (`$json.message.document !== undefined`)
- ✅ Photo detection (`$json.message.photo !== undefined`) 
- ✅ Text fallback (`{{ true }}`)
- ✅ Proper error handling without "a.ok(to)" errors

## 🛡️ ERROR PREVENTION

**Never Again:**
- Empty JavaScript assignments (`processedText = ;`)
- Missing `disabled` property on nodes
- Wrong Switch typeVersion (must be 3.2)
- Missing condition `id` fields
- Missing `combinator` in conditions
- Wrong connection format

**Always Use:**
- This exact template structure
- Incremental testing approach
- Step-by-step node addition
- Manual workflow patterns as reference