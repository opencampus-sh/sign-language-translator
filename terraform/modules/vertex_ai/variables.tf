variable "project_id" {
  description = "The ID of the project"
  type        = string
}

variable "environment" {
  description = "The environment (dev, staging, prod)"
  type        = string
}

variable "region" {
  description = "The region for deployment"
  type        = string
}

variable "model_version" {
  description = "The version of the model to deploy"
  type        = string
}

variable "model_path" {
  description = "The path to the model artifacts"
  type        = string
}

variable "machine_type" {
  description = "The machine type for the model deployment"
  type        = string
  default     = "n1-standard-2"
}

variable "min_replicas" {
  description = "Minimum number of replicas"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Maximum number of replicas"
  type        = number
  default     = 1
}

variable "accelerator_type" {
  description = "The type of accelerator to attach to the deployment"
  type        = string
  default     = null
}

variable "accelerator_count" {
  description = "The number of accelerators to attach"
  type        = number
  default     = 0
}

variable "container_image_uri" {
  description = "The URI of the container image to use"
  type        = string
} 
