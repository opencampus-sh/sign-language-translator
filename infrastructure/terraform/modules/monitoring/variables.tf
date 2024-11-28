variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "environment" {
  description = "The environment (dev, staging, prod)"
  type        = string
}

variable "enable_budget_alerts" {
  description = "Enable budget alerts"
  type        = bool
  default     = false
}

# Add a variable to control alert creation
variable "enable_vertex_ai_alerts" {
  description = "Enable Vertex AI monitoring alerts. Only enable after endpoint is deployed and receiving traffic."
  type        = bool
  default     = false
}

variable "vertex_ai_endpoint_id" {
  description = "The ID of the Vertex AI endpoint to monitor"
  type        = string
  default     = ""
}

variable "notification_email" {
  description = "Email address for alert notifications"
  type        = string
  default     = null
}

variable "alert_thresholds" {
  description = "Thresholds for different alerts"
  type = object({
    latency_threshold    = number
    error_rate_threshold = number
  })
  default = {
    latency_threshold    = 1000 # 1 second
    error_rate_threshold = 0.05 # 5%
  }
}

variable "billing_account_id" {
  description = "The ID of the billing account"
  type        = string
  default     = null
}

variable "budget_amount" {
  description = "Monthly budget amount in USD"
  type        = number
  default     = null
}

variable "cost_alert_threshold" {
  description = "Threshold for hourly cost alerts in USD"
  type        = number
  default     = 5 # $5 per hour
}
