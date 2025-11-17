# Azure DevOps & Azure Web App Deployment Guide
## AI-Audit-App - Complete Deployment Instructions

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Overview](#project-overview)
3. [Local Setup](#local-setup)
4. [Azure Resources Setup](#azure-resources-setup)
5. [Azure DevOps Setup](#azure-devops-setup)
6. [Configure CI/CD Pipeline](#configure-cicd-pipeline)
7. [Configure Environment Variables](#configure-environment-variables)
8. [Deploy to Azure](#deploy-to-azure)
9. [Post-Deployment Testing](#post-deployment-testing)
10. [Troubleshooting](#troubleshooting)
11. [Local Development](#local-development)

---

## Prerequisites

Before you begin, ensure you have:

### Required Accounts & Services
- ✅ **Microsoft Azure Account** with active subscription
- ✅ **Azure DevOps Account** (free tier is sufficient)
- ✅ **Azure OpenAI Resource** with deployed model
- ✅ **Gmail Account** with App Password enabled
- ✅ **Git** installed on your Mac
- ✅ **Python 3.12** installed on your Mac

### Required Access
- ✅ Azure subscription with permission to create resources
- ✅ Azure DevOps organization access
- ✅ Ability to create service connections in Azure DevOps

---

## Project Overview

### What This App Does
The AI-Audit-App is a FastAPI web application that:
1. Receives company data via webhook from Google Sheets
2. Analyzes the data using Azure OpenAI
3. Generates professional PDF audit reports
4. Sends reports via email

### Technology Stack
- **Backend:** Python 3.12 + FastAPI
- **AI:** Microsoft Azure OpenAI
- **PDF Generation:** ReportLab + Matplotlib
- **Email:** SMTP (Gmail)
- **Hosting:** Azure Web App (Linux)
- **CI/CD:** Azure DevOps Pipelines

### Architecture (After Deployment)
```
Google Sheets → Azure Web App → Azure OpenAI → Email
                     ↓
              (No ngrok needed!)
```

---

## Local Setup

### 1. Install Python 3.12 (if not already installed)

Check your Python version:
```bash
python3 --version
```

If you need to install Python 3.12:
```bash
# Using Homebrew on Mac
brew install python@3.12
```

### 2. Clone or Navigate to Your Project

```bash
cd ~/path/to/AI-Audit-App
```

### 3. Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
nano .env
```

**Required Configuration:**
```bash
# Azure OpenAI (from Azure Portal)
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Email (Gmail App Password)
SENDER_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
```

### 6. Test Locally (Optional)

```bash
# Test Azure OpenAI connection
python test_azure_openai.py

# Run the application
python main.py

# In another terminal, test the health endpoint
curl http://localhost:8000/health
```

---

## Azure Resources Setup

### Step 1: Create Azure Web App

1. **Login to Azure Portal:**
   - Go to https://portal.azure.com
   - Login with your Microsoft account

2. **Create Web App:**
   - Click **"Create a resource"**
   - Search for **"Web App"**
   - Click **"Create"**

3. **Configure Web App:**
   ```
   Basics:
   - Subscription: Your Azure subscription
   - Resource Group: Create new (e.g., "rg-ai-audit-app")
   - Name: Choose a unique name (e.g., "ai-audit-app-prod")
     This will be: https://ai-audit-app-prod.azurewebsites.net
   - Publish: Code
   - Runtime stack: Python 3.12
   - Operating System: Linux
   - Region: Choose closest to you (e.g., East US, West Europe)
   
   App Service Plan:
   - Create new plan
   - Pricing tier: Basic B1 (or higher for production)
   ```

4. **Review and Create:**
   - Click **"Review + create"**
   - Click **"Create"**
   - Wait for deployment to complete (2-3 minutes)

5. **Note Your Web App URL:**
   ```
   https://[your-app-name].azurewebsites.net
   ```

### Step 2: Verify Azure OpenAI Resource

Ensure you have Azure OpenAI already set up:

1. **Go to Azure Portal → Your OpenAI Resource**
2. **Note the following:**
   - Endpoint URL (e.g., `https://your-resource.cognitiveservices.azure.com/`)
   - API Key (from "Keys and Endpoint" section)
   - Deployment name (from "Deployments" section)

### Step 3: Get Gmail App Password

1. **Enable 2-Step Verification:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification if not already enabled

2. **Create App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - App name: "AI Audit App"
   - Click "Generate"
   - **Copy the 16-character password** (you'll need this later)

---

## Azure DevOps Setup

### Step 1: Create Azure DevOps Organization

1. **Go to Azure DevOps:**
   - Visit https://dev.azure.com
   - Sign in with your Microsoft account

2. **Create Organization (if needed):**
   - Click **"New organization"**
   - Choose a name (e.g., "your-company")
   - Select region
   - Click **"Continue"**

### Step 2: Create Project

1. **In Azure DevOps, click "New Project":**
   ```
   Project name: AI-Audit-App
   Visibility: Private
   Version control: Git
   Work item process: Agile
   ```

2. **Click "Create"**

### Step 3: Connect Your Git Repository

**Option A: Push Your Local Code to Azure DevOps**

1. **Initialize Git (if not already done):**
   ```bash
   cd ~/path/to/AI-Audit-App
   git init
   git add .
   git commit -m "Initial commit for Azure deployment"
   ```

2. **Add Azure DevOps as remote:**
   ```bash
   # Get the URL from Azure DevOps > Repos > Files > "Clone"
   git remote add origin https://dev.azure.com/your-org/AI-Audit-App/_git/AI-Audit-App
   ```

3. **Push to Azure DevOps:**
   ```bash
   git push -u origin main
   ```

   If asked for credentials:
   - Username: Your Azure DevOps email
   - Password: Generate a Personal Access Token (PAT):
     - Azure DevOps → User Settings → Personal Access Tokens
     - New Token → Full access → Create
     - Use this token as password

**Option B: Import from GitHub (if already on GitHub)**

1. **In Azure DevOps → Repos → Import:**
   - Source type: Git
   - Clone URL: Your GitHub repository URL
   - Requires authentication: Yes (if private)
   - Click "Import"

---

## Configure CI/CD Pipeline

### Step 1: Create Service Connection

This allows Azure DevOps to deploy to your Azure Web App.

1. **In Azure DevOps → Project Settings → Service connections:**
   - Click **"New service connection"**
   - Choose **"Azure Resource Manager"**
   - Click **"Next"**

2. **Authentication method:**
   - Choose **"Service principal (automatic)"**
   - Click **"Next"**

3. **Configure connection:**
   ```
   Scope level: Subscription
   Subscription: Your Azure subscription
   Resource group: rg-ai-audit-app (or your resource group)
   Service connection name: azure-ai-audit-connection
   Grant access to all pipelines: ✅ Checked
   ```

4. **Click "Save"**

### Step 2: Update Pipeline Configuration

1. **Edit `azure-pipelines.yml` in your project:**
   ```bash
   nano azure-pipelines.yml
   ```

2. **Update these variables:**
   ```yaml
   variables:
     pythonVersion: '3.12'
     azureWebAppName: 'ai-audit-app-prod'  # Your Web App name
     azureServiceConnection: 'azure-ai-audit-connection'  # Your service connection name
   ```

3. **Commit and push:**
   ```bash
   git add azure-pipelines.yml
   git commit -m "Configure Azure pipeline"
   git push
   ```

### Step 3: Create Pipeline in Azure DevOps

1. **In Azure DevOps → Pipelines → Create Pipeline:**
   - Click **"Create Pipeline"**

2. **Where is your code?**
   - Select **"Azure Repos Git"**
   - Choose your repository: **AI-Audit-App**

3. **Configure your pipeline:**
   - Select **"Existing Azure Pipelines YAML file"**
   - Path: `/azure-pipelines.yml`
   - Click **"Continue"**

4. **Review and Run:**
   - Review the YAML configuration
   - Click **"Run"**
   - The pipeline will start building

---

## Configure Environment Variables

**IMPORTANT:** Environment variables must be set in Azure Web App, not in your code!

### Step 1: Configure Web App Settings

1. **Go to Azure Portal → Your Web App**

2. **Navigate to Configuration:**
   - In left menu: **Configuration**
   - Click **"Application settings"**

3. **Add Environment Variables:**

Click **"+ New application setting"** for each variable:

| Name | Value | Example |
|------|-------|---------|
| `AZURE_OPENAI_ENDPOINT` | Your OpenAI endpoint | `https://your-resource.cognitiveservices.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Your OpenAI API key | `abc123...` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Your deployment name | `gpt-4o-mini` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-12-01-preview` |
| `SENDER_EMAIL` | Your Gmail address | `your-email@gmail.com` |
| `SMTP_PASSWORD` | Gmail app password | `abcd efgh ijkl mnop` |
| `SMTP_HOST` | SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `465` |
| `LOG_LEVEL` | Logging level | `INFO` |

4. **Save Configuration:**
   - Click **"Save"** at the top
   - Click **"Continue"** when prompted
   - Wait for Web App to restart (1-2 minutes)

### Step 2: Configure Startup Command

1. **Still in Configuration → General settings:**
   ```
   Startup Command: uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Save changes**

---

## Deploy to Azure

### Option 1: Automatic Deployment (CI/CD)

The pipeline will automatically deploy when you push to the `main` branch.

1. **Make any code change:**
   ```bash
   git add .
   git commit -m "Trigger deployment"
   git push
   ```

2. **Monitor Pipeline:**
   - Go to Azure DevOps → Pipelines
   - Click on running pipeline
   - Watch the build and deploy stages
   - Deployment typically takes 3-5 minutes

3. **Verify Deployment:**
   - When complete, status will show "✓ Success"
   - Your app is now live at: `https://[your-app-name].azurewebsites.net`

### Option 2: Manual Deployment (from Azure DevOps)

1. **Go to Azure DevOps → Pipelines**
2. **Click on your pipeline**
3. **Click "Run pipeline"**
4. **Select branch: `main`**
5. **Click "Run"**

### Option 3: Manual Deployment (ZIP Deploy)

For quick testing without CI/CD:

1. **Create deployment package:**
   ```bash
   cd ~/path/to/AI-Audit-App
   
   # Remove unnecessary files
   rm -rf __pycache__ venv .git
   
   # Create ZIP
   zip -r deploy.zip . -x "*.git*" -x "*__pycache__*" -x "*.env" -x "venv/*"
   ```

2. **Deploy via Azure CLI:**
   ```bash
   # Install Azure CLI (if needed)
   brew install azure-cli
   
   # Login
   az login
   
   # Deploy
   az webapp deployment source config-zip \
     --resource-group rg-ai-audit-app \
     --name ai-audit-app-prod \
     --src deploy.zip
   ```

---

## Post-Deployment Testing

### Step 1: Check Health Endpoint

```bash
# Replace with your actual Web App URL
curl https://ai-audit-app-prod.azurewebsites.net/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-17T12:00:00.000Z",
  "service": "AI Audit Agent"
}
```

### Step 2: Check Application Logs

1. **In Azure Portal → Your Web App → Log stream:**
   - You should see application startup logs
   - Check for any errors

2. **Or use Azure CLI:**
   ```bash
   az webapp log tail \
     --resource-group rg-ai-audit-app \
     --name ai-audit-app-prod
   ```

### Step 3: Test Webhook Endpoint

```bash
curl -X POST https://ai-audit-app-prod.azurewebsites.net/webhook/sheet-row \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "recipient_name": "Test User",
    "recipient_email": "your-test-email@gmail.com",
    "industry": "Technology",
    "company_size": "50-100 employees",
    "annual_revenue_inr": "10 Cr",
    "departments": {
      "IT": {
        "current_tools": "Basic tools",
        "automation_level": "Low"
      }
    }
  }'
```

**Expected Response:**
```json
{
  "status": "accepted",
  "message": "Audit request accepted and being processed for Test Company",
  "request_id": "audit_20251117_120000",
  "timestamp": "2025-11-17T12:00:00.000Z"
}
```

### Step 4: Update Google Sheets Webhook

Update your Google Sheets Apps Script with the new URL:

```javascript
// Replace the old ngrok URL with your Azure Web App URL
const WEBHOOK_URL = "https://ai-audit-app-prod.azurewebsites.net/webhook/sheet-row";
```

---

## Troubleshooting

### Issue: "Application Error" on Web App URL

**Causes:**
- Missing environment variables
- Incorrect startup command
- Dependencies not installed

**Solutions:**
1. **Check Configuration:**
   - Azure Portal → Web App → Configuration
   - Verify all environment variables are set

2. **Check Startup Command:**
   - Configuration → General settings
   - Should be: `uvicorn main:app --host 0.0.0.0 --port 8000`

3. **Check Logs:**
   ```bash
   az webapp log tail --resource-group rg-ai-audit-app --name ai-audit-app-prod
   ```

4. **Restart Web App:**
   - Azure Portal → Your Web App → Restart

### Issue: Pipeline Fails to Deploy

**Common Causes:**
- Service connection not configured
- Wrong Web App name in pipeline YAML
- Insufficient permissions

**Solutions:**
1. **Verify Service Connection:**
   - Azure DevOps → Project Settings → Service connections
   - Test the connection

2. **Check Pipeline Variables:**
   - Verify `azureWebAppName` matches your actual Web App name
   - Verify `azureServiceConnection` matches your service connection name

3. **Check Permissions:**
   - Ensure service principal has "Contributor" role on resource group

### Issue: Health Check Returns 404

**Causes:**
- Application didn't start correctly
- Port mismatch

**Solutions:**
1. **Check if app is running:**
   - Azure Portal → Web App → Log stream
   - Look for "Application startup complete"

2. **Verify startup command:**
   - Should include `--port 8000`

### Issue: "Cannot Connect to Azure OpenAI"

**Causes:**
- Incorrect endpoint or API key
- Environment variables not set

**Solutions:**
1. **Verify in Azure Portal:**
   - Go to your Azure OpenAI resource
   - Keys and Endpoint → Copy fresh values

2. **Update Web App Configuration:**
   - Configuration → Application settings
   - Update `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`
   - Save and restart

### Issue: "Email Not Sent"

**Causes:**
- Incorrect Gmail App Password
- Gmail blocking login

**Solutions:**
1. **Generate New App Password:**
   - https://myaccount.google.com/apppasswords
   - Create new password
   - Update `SMTP_PASSWORD` in Web App configuration

2. **Check Email Settings:**
   - Verify `SMTP_HOST=smtp.gmail.com`
   - Verify `SMTP_PORT=465`

### Issue: "Module Not Found" Error

**Causes:**
- Dependencies not installed
- Wrong Python version

**Solutions:**
1. **Verify requirements.txt is included:**
   ```bash
   git ls-files | grep requirements.txt
   ```

2. **Check Python version:**
   - Azure Portal → Web App → Configuration → General settings
   - Runtime: Python 3.12

3. **Redeploy:**
   ```bash
   git commit --allow-empty -m "Trigger redeploy"
   git push
   ```

---

## Local Development

### Running Locally (Without Azure)

1. **Activate virtual environment:**
   ```bash
   cd ~/path/to/AI-Audit-App
   source venv/bin/activate
   ```

2. **Ensure .env is configured:**
   ```bash
   cat .env
   # Verify all variables are set
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Access locally:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

### Making Changes

1. **Edit code locally**

2. **Test locally:**
   ```bash
   python main.py
   # Test your changes
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```

4. **Pipeline automatically deploys to Azure**

### Local Testing with Docker (Optional)

1. **Build Docker image:**
   ```bash
   docker build -t ai-audit-app .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 --env-file .env ai-audit-app
   ```

3. **Test:**
   ```bash
   curl http://localhost:8000/health
   ```

---

## Environment Variables Reference

### Azure OpenAI Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI resource endpoint | `https://myresource.cognitiveservices.azure.com/` |
| `AZURE_OPENAI_API_KEY` | API key from Azure Portal | `abc123def456...` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | `gpt-4o-mini` or `gpt-35-turbo` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-12-01-preview` |

### Email Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `SENDER_EMAIL` | Gmail address for sending emails | `your-email@gmail.com` |
| `SMTP_PASSWORD` | Gmail App Password (16 chars) | `abcd efgh ijkl mnop` |
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (SSL) | `465` |

### Application Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level | `INFO` |
| `OUTPUT_DIR` | Temporary PDF storage | `/tmp/ai_audit_reports` |

---

## Cost Estimates

### Azure Web App
- **Basic B1:** ~$13/month
- **Standard S1:** ~$70/month (recommended for production)

### Azure OpenAI
- **GPT-3.5-Turbo:** ~$0.004 per audit
- **GPT-4o-mini:** ~$0.006 per audit

### Total Monthly Cost (Estimate)
- **Web App (Basic):** $13
- **OpenAI (100 audits/month):** $0.60
- **Total:** ~$14/month

---

## Security Best Practices

### ✅ DO:
- ✅ Store secrets in Azure Web App Configuration
- ✅ Use `.gitignore` to exclude `.env` files
- ✅ Enable HTTPS (automatic on Azure Web App)
- ✅ Rotate API keys regularly
- ✅ Use Azure Key Vault for production
- ✅ Enable Azure Web App authentication if needed

### ❌ DON'T:
- ❌ Commit `.env` files to Git
- ❌ Hard-code API keys in code
- ❌ Share API keys via email or chat
- ❌ Use personal Gmail passwords (use App Passwords)
- ❌ Disable HTTPS

---

## Summary: Complete Deployment Checklist

### Pre-Deployment
- [ ] Python 3.12 installed on Mac
- [ ] Azure OpenAI resource created and configured
- [ ] Gmail App Password generated
- [ ] Git repository initialized

### Azure Setup
- [ ] Azure Web App created (Python 3.12, Linux)
- [ ] Azure DevOps organization and project created
- [ ] Service connection configured
- [ ] Environment variables set in Web App configuration

### Code Repository
- [ ] Code pushed to Azure DevOps
- [ ] `azure-pipelines.yml` configured with correct values
- [ ] `.gitignore` in place (no secrets in Git)
- [ ] `.env.example` created as template

### Deployment
- [ ] Pipeline created in Azure DevOps
- [ ] First deployment successful
- [ ] Health endpoint responds
- [ ] Application logs show no errors

### Testing
- [ ] Health check returns 200 OK
- [ ] Test webhook request successful
- [ ] Email received with PDF attachment
- [ ] Google Sheets webhook updated with new URL

### Post-Deployment
- [ ] Monitoring enabled
- [ ] Documentation updated with URLs
- [ ] Team trained on deployment process
- [ ] Backup and disaster recovery plan in place

---

## Additional Resources

### Azure Documentation
- Azure Web App: https://docs.microsoft.com/azure/app-service/
- Azure DevOps: https://docs.microsoft.com/azure/devops/
- Azure OpenAI: https://docs.microsoft.com/azure/cognitive-services/openai/

### Support
- Azure Portal: https://portal.azure.com
- Azure DevOps: https://dev.azure.com
- Project Documentation: See `docs/` folder

---

## Quick Reference Commands

```bash
# Local Development
python main.py                    # Run locally
python test_azure_openai.py      # Test Azure connection

# Git Operations
git add .                         # Stage changes
git commit -m "message"          # Commit changes
git push                          # Deploy to Azure (via pipeline)

# Azure CLI
az login                          # Login to Azure
az webapp log tail --resource-group rg-ai-audit-app --name ai-audit-app-prod
az webapp restart --resource-group rg-ai-audit-app --name ai-audit-app-prod

# Testing
curl https://your-app.azurewebsites.net/health
curl https://your-app.azurewebsites.net/docs
```

---

**Congratulations! Your AI-Audit-App is now deployed to Azure! 🎉**

**Your app is accessible at:** `https://[your-app-name].azurewebsites.net`

**No more ngrok needed!** The app runs 24/7 on Azure infrastructure.

---

*Last Updated: November 17, 2025*  
*Version: 1.0*
