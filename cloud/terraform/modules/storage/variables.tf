variable "project_id" {
  description = "The ID of the project"
  type        = string
}

variable "region" {
  description = "The region to create resources in"
  type        = string
  default     = "europe-west3"
}

variable "environment" {
  description = "The environment (dev or staging)"
  type        = string
}