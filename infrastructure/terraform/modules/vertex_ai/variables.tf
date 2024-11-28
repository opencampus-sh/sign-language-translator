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
}

variable "service_account_email" {
  description = "Email of the Vertex AI service account"
  type        = string
  default     = "" # Make it optional
}
