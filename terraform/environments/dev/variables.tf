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

variable "model_version" {
  description = "Version of the model to deploy"
  type        = string
  default     = "latest" # Default for development
}

variable "model_path" {
  description = "Path to the model artifacts in GCS"
  type        = string
  default     = "models/dev-latest" # Default development model path
}

variable "github_owner" {
  description = "GitHub username or organization name"
  type        = string
}

variable "branch_name" {
  description = "Branch name to trigger builds from"
  type        = string
  default     = "main"
}

variable "cloudrun_memory_limit" {
  description = "Memory limit for Cloud Run service"
  type        = string
  default     = "2Gi"
}

variable "cloudrun_cpu_limit" {
  description = "CPU limit for Cloud Run service"
  type        = string
  default     = "1000m"
}

variable "notification_email" {
  description = "Email address for monitoring notifications"
  type        = string
}
