#!/bin/bash

# Deploy n8n Telegram AI Assistant Workflow
# This script deploys the workflow directly through n8n's API

set -e

ADMIN_DIR="/home/ubuntu/claude-prompts/admin"
N8N_URL="http://localhost:5678"
WORKFLOW_FILE="$ADMIN_DIR/telegram-ai-workflow-complete.json"

echo "🚀 n8n Telegram AI Assistant Workflow Deployment"
echo "================================================="

# Check if n8n is running
if ! curl -s "$N8N_URL" > /dev/null; then
    echo "❌ n8n is not accessible at $N8N_URL"
    echo "Please ensure n8n is running and try again"
    exit 1
fi

echo "✅ n8n is accessible at $N8N_URL"

# Check if workflow file exists
if [[ ! -f "$WORKFLOW_FILE" ]]; then
    echo "❌ Workflow file not found: $WORKFLOW_FILE"
    exit 1
fi

echo "✅ Workflow file found: $WORKFLOW_FILE"

# Function to get credentials
get_credentials() {
    echo "🔍 Checking existing credentials..."
    
    # Try to get credentials (might fail if auth required)
    CREDS_RESPONSE=$(curl -s "$N8N_URL/rest/credentials" 2>/dev/null || echo '{"status":"error"}')
    
    if echo "$CREDS_RESPONSE" | grep -q '"status":"error"'; then
        echo "⚠️  Cannot access credentials API (authentication may be required)"
        echo "Please ensure you have Telegram credentials configured in n8n with name: 'Telegram Bot API'"
        return 1
    fi
    
    # Check if Telegram credentials exist
    TELEGRAM_CRED_ID=$(echo "$CREDS_RESPONSE" | jq -r '.[] | select(.type=="telegramApi") | .id' | head -1)
    
    if [[ -n "$TELEGRAM_CRED_ID" && "$TELEGRAM_CRED_ID" != "null" ]]; then
        echo "✅ Found Telegram credentials (ID: $TELEGRAM_CRED_ID)"
        return 0
    else
        echo "❌ No Telegram credentials found"
        return 1
    fi
}

# Function to update workflow with credential IDs
update_workflow_credentials() {
    local cred_id="$1"
    echo "🔧 Updating workflow with credential ID: $cred_id"
    
    # Use sed to replace placeholder credential ID
    sed "s/telegram_credentials_id/$cred_id/g" "$WORKFLOW_FILE" > "$WORKFLOW_FILE.tmp"
    mv "$WORKFLOW_FILE.tmp" "$WORKFLOW_FILE"
    
    echo "✅ Workflow updated with credential references"
}

# Function to deploy workflow
deploy_workflow() {
    echo "📤 Deploying workflow to n8n..."
    
    # Read workflow JSON
    WORKFLOW_JSON=$(cat "$WORKFLOW_FILE")
    
    # Try to create workflow
    DEPLOY_RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$WORKFLOW_JSON" \
        "$N8N_URL/rest/workflows" 2>/dev/null || echo '{"status":"error"}')
    
    if echo "$DEPLOY_RESPONSE" | grep -q '"id"'; then
        WORKFLOW_ID=$(echo "$DEPLOY_RESPONSE" | jq -r '.id')
        echo "✅ Workflow deployed successfully! ID: $WORKFLOW_ID"
        echo "🌐 Workflow URL: $N8N_URL/workflow/$WORKFLOW_ID"
        return 0
    else
        echo "❌ Failed to deploy workflow"
        echo "Response: $DEPLOY_RESPONSE"
        return 1
    fi
}

# Function to activate workflow
activate_workflow() {
    local workflow_id="$1"
    echo "🔄 Activating workflow..."
    
    ACTIVATE_RESPONSE=$(curl -s -X POST \
        "$N8N_URL/rest/workflows/$workflow_id/activate" 2>/dev/null || echo '{"status":"error"}')
    
    if echo "$ACTIVATE_RESPONSE" | grep -q '"active":true'; then
        echo "✅ Workflow activated successfully!"
        return 0
    else
        echo "⚠️  Could not activate workflow automatically"
        echo "Please activate it manually in the n8n interface"
        return 1
    fi
}

# Main deployment process
main() {
    echo "🔍 Step 1: Checking prerequisites..."
    
    # Check if jq is available for JSON processing
    if ! command -v jq &> /dev/null; then
        echo "Installing jq for JSON processing..."
        sudo apt-get update && sudo apt-get install -y jq
    fi
    
    echo "🔑 Step 2: Checking credentials..."
    if get_credentials; then
        TELEGRAM_CRED_ID=$(curl -s "$N8N_URL/rest/credentials" | jq -r '.[] | select(.type=="telegramApi") | .id' | head -1)
        update_workflow_credentials "$TELEGRAM_CRED_ID"
    else
        echo "⚠️  Proceeding without credential update (may need manual configuration)"
    fi
    
    echo "📦 Step 3: Deploying workflow..."
    if deploy_workflow; then
        WORKFLOW_ID=$(curl -s -X POST -H "Content-Type: application/json" -d "$WORKFLOW_JSON" "$N8N_URL/rest/workflows" | jq -r '.id')
        
        echo "🔄 Step 4: Activating workflow..."
        activate_workflow "$WORKFLOW_ID"
        
        echo ""
        echo "🎉 Deployment Complete!"
        echo "========================"
        echo "Workflow Name: Telegram AI Assistant - Voice/File/Image (Complete)"
        echo "Workflow ID: $WORKFLOW_ID"
        echo "n8n URL: $N8N_URL/workflow/$WORKFLOW_ID"
        echo ""
        echo "📋 Next Steps:"
        echo "1. Open n8n interface: $N8N_URL"
        echo "2. Navigate to your workflow"
        echo "3. Configure Telegram Bot credentials if not already done"
        echo "4. Set up webhook URL in your Telegram bot"
        echo "5. Test with voice messages, images, and text"
        echo ""
        echo "🤖 Telegram Bot Setup:"
        echo "- Create bot with @BotFather"
        echo "- Get bot token and add to n8n credentials"
        echo "- Set webhook: https://api.telegram.org/bot<TOKEN>/setWebhook?url=<N8N_WEBHOOK_URL>"
    else
        echo "❌ Deployment failed"
        exit 1
    fi
}

# Run main function
main