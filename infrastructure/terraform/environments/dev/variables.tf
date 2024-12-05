# terraform/environments/dev/variables.tf
variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The default GCP region"
  type        = string
  default     = "europe-west3"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# Vertex AI Configuration
# Initially the Endpoint is provided with the standard Whisper-Large-V3-Turbo model.
# This can be changed to a custom model later.
variable "model_version" {
  description = "Version of the model to deploy"
  type        = string
  default     = "latest"
}

variable "model_path" {
  description = "Path to the model artifacts in GCS"
  type        = string
  default     = "models/dev-latest"
}

variable "hf_model_id" {
  description = "The Hugging Face model ID to deploy"
  type        = string
  default     = "openai/whisper-large-v3"
}

variable "hf_task" {
  description = "The Hugging Face task type"
  type        = string
  default     = "automatic-speech-recognition"
}

variable "machine_type" {
  description = "The machine type for the Vertex AI endpoint"
  type        = string
  default     = "n1-standard-4"
}

variable "accelerator_type" {
  description = "The accelerator type for the Vertex AI endpoint"
  type        = string
  default     = "NVIDIA_TESLA_T4"
}

variable "accelerator_count" {
  description = "The number of accelerators to attach"
  type        = number
  default     = 1
}

# Monitoring Configuration

# The format should be a comma-separated list of email addresses
variable "notification_email" {
  description = "Email address for monitoring notifications"
  type        = string
}

variable "enable_vertex_ai_alerts" {
  description = "Enable Vertex AI monitoring alerts. Only enable after endpoint is deployed and receiving traffic."
  type        = bool
  default     = false
}

variable "enable_budget_alerts" {
  description = "Enable budget monitoring alerts"
  type        = bool
  default     = true
}

variable "billing_account_id" {
  description = "The ID of the billing account"
  type        = string
}

variable "budget_amount" {
  description = "Monthly budget amount in USD"
  type        = number
}

variable "cost_alert_threshold" {
  description = "Threshold for hourly cost alerts in USD"
  type        = number
}

variable "github_token" {
  description = "GitHub token for Cloud Build"
  type        = string
  sensitive   = true
}

variable "github_app_installation_id" {
  description = "The installation ID of the Cloud Build GitHub App"
  type        = number # Installation IDs are numeric
}
