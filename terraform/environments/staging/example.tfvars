# Project Configuration
project_id = "your-project-id" # e.g., "sign-lang-translator-123"
region     = "europe-west3"    # e.g., "europe-west3", "us-central1"

# GitHub Configuration
github_owner = "your-github-username" # e.g., "opencampus-sh"
branch_name  = "main"                 # e.g., "main", "master", "development"

# Monitoring Configuration
notification_email = "your-email@example.com" # e.g., "admin@company.com"

# Note: The following are optional as they match the defaults in variables.tf
# cloudrun_memory_limit = "2Gi"                     # e.g., "2Gi", "512Mi"
# cloudrun_cpu_limit    = "1000m"                   # e.g., "1000m", "500m"
# environment          = "dev"                      # e.g., "dev", "staging", "prod"
