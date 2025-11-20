# 🔐 **DIGICONSULT OAUTH2 SETUP GUIDE**
## **Google & Microsoft Authentication Credentials**

---

## 📧 **EMAIL CONTENT FOR CK@DIGICONSULT.CA**

**Subject:** 🔐 DigiConsult Authentication Setup - Google & Microsoft OAuth2 Credentials Needed

---

### 🎯 **WHAT YOU NEED TO DO**

Your PocketBase authentication system is now running at **auth2.digiconsult.ca**. 

To complete the setup, you need to create OAuth2 applications with Google and Microsoft to get 4 credentials:

1. **Google Client ID**
2. **Google Client Secret** 
3. **Microsoft Client ID**
4. **Microsoft Client Secret**

**⏱️ Time Required:** 20-25 minutes total

---

## 🟦 **PART 1: GOOGLE OAUTH2 SETUP (10 minutes)**

### **Step 1: Access Google Cloud Console**
1. Go to: https://console.cloud.google.com/apis/credentials
2. Sign in with your Google account

### **Step 2: Create Project**
1. Click dropdown at top → "New Project"
2. Name: `DigiConsult Authentication`
3. Click "Create" and select the project

### **Step 3: Configure OAuth Consent Screen**
1. Left sidebar → "OAuth consent screen"
2. Choose "External" → Create
3. Fill in:
   - **App name:** DigiConsult
   - **User support email:** ck@digiconsult.ca
   - **Developer contact:** ck@digiconsult.ca
4. Click "Save and Continue" through all steps

### **Step 4: Create OAuth2 Credentials**
1. Left sidebar → "Credentials"
2. "Create Credentials" → "OAuth client ID"
3. Application type: "Web application"
4. Name: `DigiConsult Web Auth`
5. **Authorized redirect URIs:** `https://auth2.digiconsult.ca/api/oauth2-redirect`
6. Click "Create"

### **📋 SAVE THESE GOOGLE CREDENTIALS:**
- **Client ID:** (ends with .apps.googleusercontent.com)
- **Client Secret:** (random string)

---

## 🔷 **PART 2: MICROSOFT OAUTH2 SETUP (15 minutes)**

### **Step 1: Access Azure Portal**
1. Go to: https://portal.azure.com
2. Sign in with Microsoft account
3. Create free account if needed (no charges for OAuth2)

### **Step 2: App Registrations**
1. Search: `App registrations`
2. Click "App registrations"
3. Click "New registration"

### **Step 3: Register Application**
1. **Name:** DigiConsult Authentication
2. **Account types:** "Accounts in any organizational directory and personal Microsoft accounts"
3. **Redirect URI:**
   - Platform: Web
   - URL: `https://auth2.digiconsult.ca/api/oauth2-redirect`
4. Click "Register"

### **Step 4: Get Application ID**
1. Copy the **Application (client) ID** from overview page

### **Step 5: Create Client Secret**
1. Left menu → "Certificates & secrets"
2. "New client secret"
3. Description: `DigiConsult Auth Secret`
4. Expires: 24 months
5. Click "Add"
6. **IMMEDIATELY copy the "Value"** (you can't see it again!)

### **📋 SAVE THESE MICROSOFT CREDENTIALS:**
- **Application (client) ID:** (UUID format)
- **Client Secret Value:** (copy immediately!)

---

## ✅ **FINAL CHECKLIST**

You should have these 4 pieces of information:

1. ✅ **Google Client ID:** ends with .apps.googleusercontent.com
2. ✅ **Google Client Secret:** random string from Google  
3. ✅ **Microsoft Client ID:** UUID format
4. ✅ **Microsoft Client Secret:** random string from Azure

---

## 🚀 **NEXT STEPS**

**Send me these 4 credentials and I'll:**
1. Configure them in PocketBase (5 minutes)
2. Test Google login flow
3. Test Microsoft login flow  
4. Update website authentication
5. Make system live for users!

---

## 🔒 **SECURITY REMINDERS**

- Never share credentials publicly
- Don't commit to code repositories  
- Only share through secure channels
- Regenerate if accidentally exposed

---

## 📞 **NEED HELP?**

**Stuck on any step?**
- Take a screenshot
- Send it to me with your question
- I'll guide you through step-by-step

---

## 🎯 **CURRENT STATUS**

**✅ COMPLETED:**
- PocketBase deployed and running
- DNS configured for auth2.digiconsult.ca
- Caddy proxy configured
- Infrastructure ready

**🔄 WAITING FOR:**
- OAuth2 credentials from you
- Then we configure and test everything

**🎉 50% COMPLETE!** Once you get the credentials, we'll finish the authentication system setup.

---

**Ready when you are! Send me those 4 OAuth2 credentials and we'll complete the setup! 🚀**