# infrastructure/terraform/modules/vertex_ai/variables.tf

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The region for Vertex AI resources"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "endpoint_name" {
  description = "Name of the model being deployed"
  type        = string
  default     = "vertex-ai"
}

variable "network_name" {
  description = "VPC network name for Vertex AI endpoint"
  type        = string
  default     = "default"
}

variable "service_account_email" {
  description = "Email of the Vertex AI service account"
  type        = string
  default     = "" # Make it optional
}

variable "github_app_installation_id" {
  description = "The installation ID of the Cloud Build GitHub App"
  type        = string
}

variable "github_token_secret_version" {
  description = "The Secret Manager version containing the GitHub token"
  type        = string
}

variable "github_owner" {
  description = "GitHub username or organization name"
  type        = string
  default     = "opencampus-sh"
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "sign-language-translator"
}

variable "model_id" {
  description = "ID of the model to deploy"
  type        = string
}

variable "model_version" {
  description = "Version of the model to deploy"
  type        = string
  default     = "latest"
}

variable "hf_task" {
  description = "Hugging Face task type"
  type        = string
  default     = "automatic-speech-recognition"
}

variable "module_depends_on" {
  description = "List of modules or resources this module depends on"
  type        = any
  default     = []
}
