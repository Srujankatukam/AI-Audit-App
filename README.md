# AI-Audit-App 
### Automated AI Maturity Audit Report Generation System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange.svg)](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---  
 
## 🎯 Overview

AI-Audit-App is an intelligent web application that automatically generates comprehensive AI maturity audit reports for companies. It receives company data via webhook, analyzes it using Azure OpenAI, creates professional PDF reports with visualizations, and delivers them via email.

### Key Features
- 🤖 **AI-Powered Analysis** using Azure OpenAI (GPT-4o-mini/GPT-3.5-Turbo)
- 📊 **Professional PDF Reports** with charts and visualizations
- 📧 **Automated Email Delivery** with personalized content
- 🔗 **Google Sheets Integration** via webhook
- ☁️ **Cloud-Native** deployment on Azure Web App
- 🚀 **CI/CD Pipeline** with Azure DevOps
- 🔒 **Secure** environment variable management

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Google Sheets  │
└────────┬────────┘
         │ Webhook (HTTPS)
         ▼
┌─────────────────────────────┐
│   Azure Web App (Linux)     │
│  ┌───────────────────────┐  │
│  │   FastAPI Backend     │  │
│  │   (Python 3.12)       │  │
│  └───────────┬───────────┘  │
│              │               │
│     ┌────────┴────────┐      │
│     ▼                 ▼      │
│ ┌────────┐      ┌──────────┐│
│ │  LLM   │      │   PDF    ││
│ │ Client │      │ Builder  ││
│ └───┬────┘      └────┬─────┘│
└─────┼────────────────┼──────┘
      │                │
      ▼                ▼
┌──────────────┐  ┌──────────┐
│ Azure OpenAI │  │  Mailer  │
└──────────────┘  └────┬─────┘
                       │
                       ▼
                 ┌──────────┐
                 │  Email   │
                 │ Recipient│
                 └──────────┘
```

---

## 📋 Prerequisites

### Required
- **Python 3.12+**
- **Azure Account** with active subscription
- **Azure OpenAI Resource** with deployed model
- **Azure DevOps Account** (for CI/CD)
- **Gmail Account** with App Password enabled
- **Git** installed

### Optional
- Docker and Docker Compose (for local container testing)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://dev.azure.com/your-org/AI-Audit-App/_git/AI-Audit-App
cd AI-Audit-App
```

### 2. Install Dependencies

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env  # or use any text editor
```

**Required Environment Variables:**
```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Email (Gmail)
SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

### 4. Test Configuration

```bash
# Test Azure OpenAI connection
python test_azure_openai.py

# Expected output: ✅ All tests passed
```

### 5. Run Application

```bash
# Start the server
python main.py

# Application will start on http://localhost:8000
```

### 6. Test API

```bash
# Health check
curl http://localhost:8000/health

# API Documentation
open http://localhost:8000/docs
```

---

## 📦 Project Structure

```
AI-Audit-App/
├── 📄 Core Application Files
│   ├── main.py                 # FastAPI application entry point
│   ├── llm_client.py           # Azure OpenAI client
│   ├── pdf_builder.py          # PDF report generator
│   ├── mailer.py               # Email service
│   └── prompt_templates.py     # LLM prompt templates
│
├── ⚙️ Configuration Files
│   ├── .env                    # Your secrets (NOT in Git)
│   ├── .env.example            # Environment template
│   ├── requirements.txt        # Python dependencies
│   ├── azure-pipelines.yml     # CI/CD pipeline configuration
│   ├── Dockerfile              # Container image definition
│   ├── docker-compose.yml      # Docker compose configuration
│   ├── startup.sh              # Azure Web App startup script
│   └── .gitignore              # Git ignore rules
│
├── 🧪 Testing Files
│   ├── test_azure_openai.py    # Test Azure OpenAI connection
│   └── test_example.py         # End-to-end test
│
├── 📚 Documentation
│   ├── README.md                       # This file
│   ├── AZURE_DEPLOYMENT_GUIDE.md       # Complete deployment guide
│   ├── PROJECT_SUMMARY.md              # Project overview
│   ├── PROJECT_STRUCTURE.md            # Architecture details
│   ├── QUICK_START.md                  # Quick start guide
│   └── docs/
│       ├── API_DOCUMENTATION.md        # API reference
│       ├── DEPLOYMENT_GUIDE.md         # General deployment
│       ├── TESTING_GUIDE.md            # Testing procedures
│       ├── GOOGLE_SHEETS_SETUP.md      # Google Sheets integration
│       ├── SAMPLE_INPUT.json           # Example request
│       └── SAMPLE_OUTPUT.json          # Example response
│
└── 🗑️ Cache (auto-generated, in .gitignore)
    └── __pycache__/
```

---

## 🌐 Deployment to Azure

This application is designed for deployment to **Azure Web App** with **Azure DevOps CI/CD**.

### Deployment Methods

#### Option 1: CI/CD Pipeline (Recommended)

1. **Push to Azure DevOps:**
   ```bash
   git add .
   git commit -m "Deploy to Azure"
   git push
   ```

2. **Pipeline automatically:**
   - Builds the application
   - Runs tests (optional)
   - Deploys to Azure Web App
   - Takes 3-5 minutes

3. **Your app is live at:**
   ```
   https://your-app-name.azurewebsites.net
   ```

#### Option 2: Manual Deployment

See **[AZURE_DEPLOYMENT_GUIDE.md](AZURE_DEPLOYMENT_GUIDE.md)** for complete step-by-step instructions.

### Quick Deployment Checklist

- [ ] Azure Web App created (Python 3.12, Linux)
- [ ] Environment variables configured in Azure Portal
- [ ] Azure DevOps project and pipeline set up
- [ ] Service connection configured
- [ ] Code pushed to Azure DevOps
- [ ] First deployment successful
- [ ] Health endpoint responding

**📘 For detailed deployment instructions, see [AZURE_DEPLOYMENT_GUIDE.md](AZURE_DEPLOYMENT_GUIDE.md)**

---

## 🔧 Configuration

### Azure OpenAI Configuration

Get these values from [Azure Portal](https://portal.azure.com):

1. Navigate to your Azure OpenAI resource
2. Go to "Keys and Endpoint"
3. Copy the values:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your_subscription_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini  # Or your deployment name
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### Email Configuration

Generate Gmail App Password:

1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Create App Password: https://myaccount.google.com/apppasswords
3. Copy the 16-character password

```bash
SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # Your app password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
```

---

## 🧪 Testing

### Test Azure OpenAI Connection

```bash
python test_azure_openai.py
```

**Expected Output:**
```
✅ Azure OpenAI client initialized successfully
✅ API connection successful
✅ Model deployment accessible
✅ All tests passed
```

### Test Complete Workflow

```bash
python test_example.py
```

This will:
1. Send a test audit request
2. Generate AI analysis
3. Create PDF report
4. Send email (to SENDER_EMAIL)

### Test API Endpoint

```bash
# Start server
python main.py

# In another terminal, test webhook
curl -X POST http://localhost:8000/webhook/sheet-row \
  -H "Content-Type: application/json" \
  -d @docs/SAMPLE_INPUT.json
```

### Test with Docker

```bash
# Build image
docker build -t ai-audit-app .

# Run container
docker-compose up

# Test health
curl http://localhost:8000/health
```

---

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-17T12:00:00.000Z",
  "service": "AI Audit Agent"
}
```

### Audit Request Webhook
```http
POST /webhook/sheet-row
Content-Type: application/json
```

**Request Body:**
```json
{
  "company_name": "Example Corp",
  "recipient_name": "John Doe",
  "recipient_email": "john@example.com",
  "industry": "Technology",
  "company_size": "50-100 employees",
  "annual_revenue_inr": "10 Cr",
  "departments": {
    "IT": {
      "current_tools": "Basic office suite",
      "automation_level": "Low"
    }
  }
}
```

**Response:**
```json
{
  "status": "accepted",
  "message": "Audit request accepted and being processed for Example Corp",
  "request_id": "audit_20251117_120000",
  "timestamp": "2025-11-17T12:00:00.000Z"
}
```

### API Documentation (Swagger)
```http
GET /docs
```

Interactive API documentation available at `/docs` when server is running.

---

## 🔒 Security

### Environment Variables
- ✅ **NEVER commit** `.env` files to Git
- ✅ Store secrets in Azure Web App Configuration
- ✅ Use `.env.example` as a template only
- ✅ Rotate API keys regularly

### Production Security
- ✅ HTTPS is enabled by default on Azure Web App
- ✅ Use Azure Key Vault for secrets (recommended)
- ✅ Enable Azure Web App authentication if needed
- ✅ Use managed identities when possible
- ✅ Monitor access logs

### .gitignore Protection
The `.gitignore` file protects:
- Environment files (`.env`, `*.env`)
- Python cache (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Logs (`*.log`, `logs/`)
- Generated PDFs (`*.pdf`)
- IDE settings (`.vscode/`, `.idea/`)

---

## 📊 Cost Estimates

### Monthly Costs (Approximate)

| Service | Tier | Cost/Month | Notes |
|---------|------|------------|-------|
| Azure Web App | Basic B1 | $13 | Entry-level |
| Azure Web App | Standard S1 | $70 | Recommended for production |
| Azure OpenAI | GPT-3.5-Turbo | $0.004/audit | ~$0.40 for 100 audits |
| Azure OpenAI | GPT-4o-mini | $0.006/audit | ~$0.60 for 100 audits |

**Typical Monthly Cost:**
- Web App (Basic) + OpenAI (100 audits): **~$14/month**
- Web App (Standard) + OpenAI (500 audits): **~$73/month**

---

## 📚 Documentation

### Getting Started
- **[README.md](README.md)** - This file (overview and quick start)
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project summary

### Deployment
- **[AZURE_DEPLOYMENT_GUIDE.md](AZURE_DEPLOYMENT_GUIDE.md)** - Complete Azure deployment guide
- **[docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - General deployment guide

### Integration
- **[docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md)** - Google Sheets webhook setup
- **[docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - API reference

### Testing & Troubleshooting
- **[docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - Testing procedures
- **[docs/SAMPLE_INPUT.json](docs/SAMPLE_INPUT.json)** - Example request
- **[docs/SAMPLE_OUTPUT.json](docs/SAMPLE_OUTPUT.json)** - Example response

---

## 🛠️ Development

### Local Development Setup

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd AI-Audit-App
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run application:**
   ```bash
   python main.py
   ```

4. **Make changes and test:**
   ```bash
   # Your changes here
   python test_azure_openai.py
   python main.py
   ```

5. **Commit and deploy:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push  # Triggers automatic deployment
   ```

### Development Workflow

```
Local Development → Git Push → Azure DevOps Pipeline → Azure Web App
     ↓                           ↓                         ↓
   Testing                    Build & Test              Production
```

---

## 🐛 Troubleshooting

### Common Issues

#### "Cannot connect to Azure OpenAI"
- Verify `AZURE_OPENAI_ENDPOINT` is correct
- Check `AZURE_OPENAI_API_KEY` in Azure Portal
- Ensure deployment name matches exactly

#### "Email not sent"
- Verify Gmail App Password (not regular password)
- Check 2-Step Verification is enabled
- Try generating a new App Password

#### "Application Error" on Azure
- Check environment variables in Azure Portal
- Verify startup command: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Check logs: Azure Portal → Web App → Log stream

#### "Pipeline fails to deploy"
- Verify service connection is configured
- Check Web App name in `azure-pipelines.yml`
- Ensure sufficient permissions

**For detailed troubleshooting, see [AZURE_DEPLOYMENT_GUIDE.md](AZURE_DEPLOYMENT_GUIDE.md#troubleshooting)**

---

## 📝 Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | ✅ | Azure OpenAI endpoint URL | `https://your-resource.cognitiveservices.azure.com/` |
| `AZURE_OPENAI_API_KEY` | ✅ | Azure OpenAI API key | `abc123...` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | ✅ | Model deployment name | `gpt-4o-mini` |
| `AZURE_OPENAI_API_VERSION` | ⚠️ | API version | `2024-12-01-preview` |
| `SENDER_EMAIL` | ✅ | Gmail address | `your-email@gmail.com` |
| `SMTP_PASSWORD` | ✅ | Gmail App Password | `abcd efgh ijkl mnop` |
| `SMTP_HOST` | ⚠️ | SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | ⚠️ | SMTP port | `465` |
| `LOG_LEVEL` | ❌ | Logging level | `INFO` |

Legend: ✅ Required | ⚠️ Has default | ❌ Optional

---

## 🤝 Contributing

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test:
   ```bash
   python test_azure_openai.py
   python test_example.py
   ```

3. Commit and push:
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request in Azure DevOps

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **Azure OpenAI** - AI-powered analysis
- **ReportLab** - PDF generation
- **Matplotlib** - Data visualization

---

## 📞 Support

### Documentation
- [Azure Deployment Guide](AZURE_DEPLOYMENT_GUIDE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Testing Guide](docs/TESTING_GUIDE.md)

### Resources
- Azure Portal: https://portal.azure.com
- Azure DevOps: https://dev.azure.com
- Azure OpenAI Docs: https://learn.microsoft.com/azure/cognitive-services/openai/

---

## 🎯 Quick Reference Commands

```bash
# Local Development
python main.py                      # Run application
python test_azure_openai.py        # Test Azure connection
python test_example.py              # Test full workflow

# Git Operations
git status                          # Check status
git add .                           # Stage changes
git commit -m "message"            # Commit changes
git push                            # Deploy (triggers pipeline)

# Docker
docker build -t ai-audit-app .     # Build image
docker-compose up                   # Run with Docker
docker-compose logs -f              # View logs

# Azure CLI
az login                            # Login to Azure
az webapp log tail --resource-group rg-ai-audit-app --name your-app-name
az webapp restart --resource-group rg-ai-audit-app --name your-app-name

# Testing
curl http://localhost:8000/health                    # Local health check
curl https://your-app.azurewebsites.net/health      # Production health check
```

---

**🚀 Your AI-Audit-App is ready for Azure deployment!**

**For complete deployment instructions, see [AZURE_DEPLOYMENT_GUIDE.md](AZURE_DEPLOYMENT_GUIDE.md)**

---

*Last Updated: November 17, 2025*  
*Version: 1.0*  
*Python: 3.12*  
*Platform: Azure Web App*
