# Project Configuration
project_id  = "your-project-id" # Required: Your GCP project ID where resources will be created
region      = "europe-west3"    # Optional: Default GCP region for resource deployment
environment = "dev"             # Optional: Environment name, affects resource naming and settings

# Model Configuration
model_id      = "openai/whisper-large-v3-turbo" # Optional: HuggingFace model identifier
model_version = "latest"                        # Optional: Model version to deploy
hf_task       = "automatic-speech-recognition"  # Optional: HuggingFace task type

# GitHub Configuration
github_token               = "your-github-token"    # Required: Personal access token with repo and workflow permissions
github_app_installation_id = 12345678               # Required: ID from Cloud Build GitHub App installation (it is provided in the link when you click on the Cloud Build app in your organizations GitHub Settings: https://github.com/organizations/your-organization/settings/installations/12345678)
github_owner               = "your-github-username" # Required: GitHub username or organization name

# Resource Configuration
machine_type      = "n1-standard-4"   # Optional: GCP machine type for Vertex AI endpoint
accelerator_type  = "NVIDIA_TESLA_T4" # Optional: GPU type for model inference
accelerator_count = 1                 # Optional: Number of GPUs per endpoint

# Cost Control Configuration
billing_account_id   = "ABCD-EFGH-IJKL-MNOP" # Required: Your GCP billing account ID for budget setup
budget_amount        = 1000                  # Optional: Monthly budget limit in USD
cost_alert_threshold = 5                     # Optional: Hourly cost alert threshold in USD

# Monitoring Configuration
notification_email      = "your-email@example.com" # Required: Email address for alerts and notifications
enable_vertex_ai_alerts = false                    # Optional: Enable Vertex AI monitoring alerts
enable_budget_alerts    = true                     # Optional: Enable budget monitoring alerts

# Network Configuration
network_name = "default" # Optional: VPC network name for resource deployment
