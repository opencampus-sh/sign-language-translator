# terraform/environments/dev/variables.tf
variable "project_id" {
  type        = string
  description = "The GCP project ID"
}

variable "region" {
  type        = string
  description = "The default GCP region"
}

variable "environment" {
  type        = string
  description = "Environment name (dev, prod, etc.)"
  default     = "dev"
}

variable "github_owner" {
  description = "GitHub username or organization name"
  type        = string
}

variable "branch_name" {
  description = "Branch name to trigger builds from"
  type        = string
}

variable "notification_email" {
  type        = string
  description = "Email address for monitoring notifications"
}

variable "cloudrun_memory_limit" {
  type        = string
  description = "Memory limit for Cloud Run service"
  default     = "2Gi"
}

variable "cloudrun_cpu_limit" {
  type        = string
  description = "CPU limit for Cloud Run service"
  default     = "1000m"
}

variable "model_version" {
  description = "Version of the model to deploy"
  type        = string
}
