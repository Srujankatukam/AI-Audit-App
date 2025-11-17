# Quick Deployment Reference Card
## AI-Audit-App - Azure Deployment Cheat Sheet

---

## 🚀 Quick Start (30 minutes)

### Step 1: Azure Web App (5 min)
```bash
# Azure Portal → Create Resource → Web App
Name: ai-audit-app-prod
Runtime: Python 3.12
OS: Linux
Plan: Basic B1 (or Standard S1)
```

### Step 2: Environment Variables (5 min)
```bash
# Azure Portal → Your Web App → Configuration → Application Settings
# Add these variables (click "New application setting" for each):

AZURE_OPENAI_ENDPOINT          # From Azure OpenAI resource
AZURE_OPENAI_API_KEY           # From Azure OpenAI resource
AZURE_OPENAI_DEPLOYMENT_NAME   # Your model deployment name
AZURE_OPENAI_API_VERSION       # 2024-12-01-preview
SENDER_EMAIL                   # Your Gmail
SMTP_PASSWORD                  # Gmail App Password
SMTP_HOST                      # smtp.gmail.com
SMTP_PORT                      # 465
```

### Step 3: Startup Command (1 min)
```bash
# Azure Portal → Your Web App → Configuration → General Settings
Startup Command: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 4: Azure DevOps (10 min)
```bash
# 1. Create organization and project at https://dev.azure.com
# 2. Create service connection:
#    Project Settings → Service connections → New
#    Type: Azure Resource Manager
#    Name: azure-ai-audit-connection

# 3. Push your code:
git init
git add .
git commit -m "Initial Azure deployment"
git remote add origin https://dev.azure.com/your-org/AI-Audit-App/_git/AI-Audit-App
git push -u origin main
```

### Step 5: Pipeline Configuration (5 min)
```bash
# 1. Edit azure-pipelines.yml:
variables:
  azureWebAppName: 'ai-audit-app-prod'  # Your Web App name
  azureServiceConnection: 'azure-ai-audit-connection'  # Your connection

# 2. Save and push:
git add azure-pipelines.yml
git commit -m "Configure pipeline"
git push
```

### Step 6: Create Pipeline (3 min)
```bash
# Azure DevOps → Pipelines → New Pipeline
# Choose: Azure Repos Git → Your repo
# Select: Existing YAML → /azure-pipelines.yml
# Click: Run
```

### Step 7: Test (1 min)
```bash
# After pipeline completes:
curl https://ai-audit-app-prod.azurewebsites.net/health

# Expected: {"status":"ok",...}
```

---

## 📋 Essential Commands

### Local Development
```bash
# Setup
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Then edit with your credentials

# Run
python main.py

# Test
python test_azure_openai.py
curl http://localhost:8000/health
```

### Git Operations
```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-azure-devops-url>
git push -u origin main

# Regular updates (triggers auto-deploy)
git add .
git commit -m "Your changes"
git push
```

### Azure CLI (Optional)
```bash
# Install
brew install azure-cli

# Login
az login

# View logs
az webapp log tail --resource-group rg-ai-audit-app --name ai-audit-app-prod

# Restart app
az webapp restart --resource-group rg-ai-audit-app --name ai-audit-app-prod

# Deploy ZIP (manual)
az webapp deployment source config-zip \
  --resource-group rg-ai-audit-app \
  --name ai-audit-app-prod \
  --src deploy.zip
```

### Docker (Optional - Local Testing)
```bash
# Build
docker build -t ai-audit-app .

# Run
docker-compose up

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔑 Environment Variables Quick Reference

### Azure OpenAI
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=abc123...
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

**Get from:** Azure Portal → Your OpenAI Resource → Keys and Endpoint

### Email (Gmail)
```bash
SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # 16-char App Password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
```

**Get App Password:** https://myaccount.google.com/apppasswords

---

## 🔍 Testing Checklist

### Local Testing
- [ ] `python test_azure_openai.py` → ✅ All tests pass
- [ ] `python main.py` → Server starts without errors
- [ ] `curl http://localhost:8000/health` → Returns {"status":"ok"}
- [ ] `python test_example.py` → Generates PDF and sends email

### Azure Testing
- [ ] Pipeline completes successfully
- [ ] `curl https://your-app.azurewebsites.net/health` → Returns 200 OK
- [ ] Azure Portal → Web App → Log stream → No errors
- [ ] Test webhook with sample data → Receive email with PDF

---

## 🆘 Quick Troubleshooting

### "Application Error" on Azure
```bash
# Check environment variables
Azure Portal → Web App → Configuration → Verify all variables set

# Check startup command
Configuration → General Settings → Should be:
uvicorn main:app --host 0.0.0.0 --port 8000

# Check logs
Azure Portal → Web App → Log stream
# Or:
az webapp log tail --resource-group rg-ai-audit-app --name ai-audit-app-prod

# Restart
Azure Portal → Web App → Restart
```

### Pipeline Fails
```bash
# Verify service connection
Azure DevOps → Project Settings → Service connections → Test connection

# Verify pipeline variables
azure-pipelines.yml → Check azureWebAppName and azureServiceConnection

# Check permissions
Service principal needs "Contributor" role on resource group
```

### "Cannot Connect to Azure OpenAI"
```bash
# Get fresh credentials
Azure Portal → Your OpenAI Resource → Keys and Endpoint
Copy: Endpoint and Key

# Update in Azure
Azure Portal → Web App → Configuration → Application Settings
Update: AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY
Save → Restart Web App
```

### Email Not Sent
```bash
# Generate new App Password
https://myaccount.google.com/apppasswords
Create new → Copy 16-character password

# Update in Azure
Azure Portal → Web App → Configuration
Update: SMTP_PASSWORD with new App Password
Save → Restart
```

---

## 📊 API Endpoints

### Health Check
```bash
GET https://your-app.azurewebsites.net/health

Response: {"status":"ok","timestamp":"...","service":"AI Audit Agent"}
```

### Webhook (from Google Sheets)
```bash
POST https://your-app.azurewebsites.net/webhook/sheet-row
Content-Type: application/json

{
  "company_name": "Example Corp",
  "recipient_email": "user@example.com",
  "industry": "Technology",
  "company_size": "50-100",
  "annual_revenue_inr": "10 Cr",
  "departments": {...}
}
```

### API Documentation
```bash
GET https://your-app.azurewebsites.net/docs
```

---

## 📁 File Reference

### Configuration Files
- **`.env.example`** - Template (safe to commit)
- **`.env`** - Your secrets (NEVER commit)
- **`.gitignore`** - Protects secrets
- **`requirements.txt`** - Python dependencies
- **`azure-pipelines.yml`** - CI/CD configuration
- **`Dockerfile`** - Container definition
- **`startup.sh`** - Azure startup script

### Application Files
- **`main.py`** - FastAPI app
- **`llm_client.py`** - Azure OpenAI
- **`pdf_builder.py`** - PDF generator
- **`mailer.py`** - Email service
- **`prompt_templates.py`** - Prompts

### Documentation
- **`AZURE_DEPLOYMENT_GUIDE.md`** - Complete guide
- **`README.md`** - Project overview
- **`DEPLOYMENT_SUMMARY.md`** - Changes summary
- **`AZURE_MIGRATION_COMPLETE.md`** - Migration status
- **`QUICK_DEPLOYMENT_REFERENCE.md`** - This file

---

## 🔗 Important URLs

### Azure Resources
- **Azure Portal:** https://portal.azure.com
- **Azure DevOps:** https://dev.azure.com
- **Your Web App:** https://your-app-name.azurewebsites.net

### Configuration
- **Gmail App Passwords:** https://myaccount.google.com/apppasswords
- **Gmail 2-Step:** https://myaccount.google.com/security
- **Azure OpenAI Docs:** https://learn.microsoft.com/azure/cognitive-services/openai/

### Documentation (Local)
- **Complete Guide:** `AZURE_DEPLOYMENT_GUIDE.md`
- **README:** `README.md`
- **Testing:** `docs/TESTING_GUIDE.md`

---

## 💰 Cost Reference

| Service | Tier | Monthly Cost |
|---------|------|--------------|
| Azure Web App | Basic B1 | ~$13 |
| Azure Web App | Standard S1 | ~$70 |
| Azure OpenAI | Per audit | ~$0.004-0.006 |
| **Total (Basic + 100 audits)** | | **~$14/month** |

---

## ✅ Pre-Deployment Checklist

### Azure Resources
- [ ] Azure subscription active
- [ ] Azure OpenAI resource created
- [ ] Model deployed in Azure OpenAI
- [ ] Azure Web App created (Python 3.12, Linux)

### Credentials Ready
- [ ] Azure OpenAI endpoint URL
- [ ] Azure OpenAI API key
- [ ] Azure OpenAI deployment name
- [ ] Gmail App Password generated

### Azure DevOps
- [ ] Organization created
- [ ] Project created
- [ ] Service connection configured
- [ ] Repository ready

### Configuration
- [ ] Environment variables set in Azure Web App
- [ ] Startup command configured
- [ ] `azure-pipelines.yml` updated with your values

### Code
- [ ] Code pushed to Azure DevOps
- [ ] `.gitignore` in place
- [ ] No `.env` file in Git
- [ ] Pipeline created

---

## 🎯 Success Criteria

### Deployment Successful When:
✅ Pipeline completes without errors  
✅ Health endpoint returns 200 OK  
✅ Application logs show no errors  
✅ Test webhook receives PDF via email  
✅ Google Sheets integration working  

---

## 📞 Quick Links

- **Full Guide:** [AZURE_DEPLOYMENT_GUIDE.md](AZURE_DEPLOYMENT_GUIDE.md)
- **README:** [README.md](README.md)
- **Migration Status:** [AZURE_MIGRATION_COMPLETE.md](AZURE_MIGRATION_COMPLETE.md)
- **Testing Guide:** [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)

---

**🚀 Keep this file handy during deployment!**

---

*Quick Reference Card*  
*Updated: November 17, 2025*  
*Version: 1.0*
