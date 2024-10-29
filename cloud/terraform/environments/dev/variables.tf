variable "project_id" {
  description = "The ID of the project"
  type        = string
}

variable "region" {
  description = "The region to create resources in"
  type        = string
  default     = "europe-west3"
}

variable "notification_email" {
  description = "Email address for monitoring alerts"
  type        = string
}
