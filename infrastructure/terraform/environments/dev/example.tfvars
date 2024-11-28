# Project Configuration
project_id = "your-project-id" # Required
region     = "europe-west3"    # Optional, defaults to europe-west3

# Environment
environment = "dev" # Optional, defaults to "dev"

# Model Configuration
model_version = "latest"                        # Optional, defaults to "latest"
model_path    = "models/dev-latest"             # Optional, defaults to "models/dev-latest"
hf_model_id   = "openai/whisper-large-v3-turbo" # Optional, defaults to "openai/whisper-large-v3-turbo"

# GitHub Configuration (if needed for future CI/CD)
github_owner = "your-github-username" # Required
branch_name  = "main"                 # Optional, defaults to "main"

# Resource Limits (if needed for future Cloud Run deployment)
cloudrun_memory_limit = "2Gi"   # Optional, defaults to "2Gi"
cloudrun_cpu_limit    = "1000m" # Optional, defaults to "1000m"

# Monitoring Configuration
notification_email = "your-email@example.com" # e.g., "admin@company.com"

# Cost Control Configuration
billing_account_id   = "XXXXXX-XXXXXX-XXXXXX" # Your billing account ID
budget_amount        = 100                    # $100 monthly budget for dev
cost_alert_threshold = 5                      # Alert if hourly cost exceeds $5
