# variables.tf
variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "Region for Cloud Run deployment"
}

variable "environment" {
  type        = string
  description = "Environment (dev, prod, etc.)"
}

variable "service_name" {
  type        = string
  description = "Name of the Cloud Run service"
}

variable "branch_name" {
  type        = string
  description = "Branch to trigger builds from"
  default     = "main"
}

variable "repository_name" {
  type        = string
  description = "Name of the Cloud Source Repository"
}

variable "image_tag" {
  type        = string
  description = "Tag of the container image to deploy"
  default     = "latest"
}

variable "cpu_limit" {
  type        = string
  description = "CPU limit for the Cloud Run service"
  default     = "1000m"
}

variable "memory_limit" {
  type        = string
  description = "Memory limit for the Cloud Run service"
  default     = "2Gi"
}

variable "invoker_member" {
  type        = string
  description = "IAM member to grant invoker access"
  default     = "allUsers" # Public access - modify as needed
}

variable "github_owner" {
  description = "GitHub username or organization name"
  type        = string
}
