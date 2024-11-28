variable "project_id" {
  description = "The ID of the project"
  type        = string
}

variable "environment" {
  description = "The environment (dev or staging)"
  type        = string
}

variable "region" {
  description = "The region for Cloud Run service"
  type        = string
}

variable "enable_cloud_run_iam" {
  description = "Whether to enable IAM for the Cloud Run service"
  type        = bool
  default     = true
}

variable "cloud_run_service_name" {
  description = "The name of the Cloud Run service"
  type        = string
  default     = "sign-language-translator"
}
