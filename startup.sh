# #!/bin/bash
# # Azure Web App Startup Script
# # This script is executed when the container starts

# echo "Starting AI-Audit-App..."

# # Ensure temporary directory exists
# mkdir -p /tmp/ai_audit_reports

# # Start the FastAPI application with uvicorn
# # Using production settings for Azure Web App
# exec uvicorn main:app \
#     --host 0.0.0.0 \
#     --port 8000 \
#     --workers 2 \
#     --log-level info \
#     --no-access-log \
#     --forwarded-allow-ips='*'
