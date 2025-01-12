terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0" # Latest stable version
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "project" {
  source     = "../../modules/project"
  project_id = var.project_id
}

module "storage" {
  source = "../../modules/storage"

  project_id  = var.project_id
  environment = var.environment
  region      = var.region
  depends_on  = [module.project]
}

module "iam" {
  source = "../../modules/iam"

  project_id           = var.project_id
  environment          = var.environment
  region               = var.region
  enable_cloud_run_iam = false
  github_token         = var.github_token
}

# module "vertex_ai" {
#   source = "../../modules/vertex_ai"

#   project_id                  = var.project_id
#   region                      = var.region
#   environment                 = var.environment
#   network_name                = "default"
#   service_account_email       = module.iam.vertex_ai_service_account
#   github_app_installation_id  = var.github_app_installation_id
#   github_token_secret_version = module.iam.github_token_secret_version
#   huggingface_token           = "" # default
#   model_id                    = "openai/whisper-large-v3-turbo"
#   model_version               = "v1" # default

#   depends_on = [
#     module.iam,
#     module.project
#   ]
# }

module "monitoring" {
  source = "../../modules/monitoring"

  project_id  = var.project_id
  environment = var.environment
  #vertex_ai_endpoint_id = module.vertex_ai.endpoint_id
  notification_email = var.notification_email

  enable_vertex_ai_alerts = false
  enable_budget_alerts    = false

  # Basic alerts for development
  alert_thresholds = {
    latency_threshold    = 1000 # 1 second
    error_rate_threshold = 0.05 # 5% error rate
  }

  # Cost control
  billing_account_id   = var.billing_account_id
  budget_amount        = var.budget_amount
  cost_alert_threshold = var.cost_alert_threshold

  depends_on = [
    module.project
    #module.vertex_ai
  ]
}
