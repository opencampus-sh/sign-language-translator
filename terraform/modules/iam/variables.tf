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

variable "cloud_run_service_name" {
  description = "The name of the Cloud Run service"
  type        = string
  default     = "sign-language-translator"
}
