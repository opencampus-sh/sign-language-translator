# Enable Cloud Monitoring API
resource "google_project_service" "monitoring" {
  service = "monitoring.googleapis.com"
  project = var.project_id

  disable_dependent_services = false
  disable_on_destroy         = false
}

# Vertex AI Model Monitoring
resource "google_monitoring_alert_policy" "vertex_ai_latency" {
  count = var.enable_vertex_ai_alerts && var.vertex_ai_endpoint_id != "" ? 1 : 0

  display_name = "Vertex AI ${var.environment} - High Latency"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "Prediction Latency"
    condition_threshold {
      filter          = "resource.type = \"aiplatform.googleapis.com/Endpoint\" AND resource.labels.endpoint_id = \"${var.vertex_ai_endpoint_id}\" AND metric.type = \"aiplatform.googleapis.com/endpoint/prediction_latency\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = var.alert_thresholds.latency_threshold

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_PERCENTILE_99"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email[0].name]
}

resource "google_monitoring_alert_policy" "vertex_ai_errors" {
  count = var.enable_vertex_ai_alerts && var.vertex_ai_endpoint_id != "" ? 1 : 0

  display_name = "Vertex AI ${var.environment} - High Error Rate"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "Error Rate"
    condition_threshold {
      filter          = "resource.type = \"aiplatform.googleapis.com/Endpoint\" AND resource.labels.endpoint_id = \"${var.vertex_ai_endpoint_id}\" AND metric.type = \"aiplatform.googleapis.com/endpoint/error_count\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = var.alert_thresholds.error_rate_threshold

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email[0].name]
}

# Email notification channel
resource "google_monitoring_notification_channel" "email" {
  count = var.notification_email != null ? 1 : 0

  display_name = "Email Notification Channel - ${var.environment}"
  project      = var.project_id
  type         = "email"

  labels = {
    email_address = var.notification_email
  }
}

# Budget monitoring
resource "google_billing_budget" "project_budget" {
  # Only create if budget alerts are enabled AND we have all required values
  count = var.enable_budget_alerts && var.billing_account_id != null && var.budget_amount != null ? 1 : 0

  provider = google

  billing_account = var.billing_account_id
  display_name    = "${var.environment}-budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]

    # Optional: specific services to monitor
    services = [
      "services/aiplatform.googleapis.com", # Vertex AI
      "services/storage.googleapis.com"     # Cloud Storage
    ]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(var.budget_amount) # Convert to string
    }
  }

  threshold_rules {
    threshold_percent = 0.5 # Alert at 50%
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 0.8 # Alert at 80%
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 1.0 # Alert at 100%
    spend_basis       = "CURRENT_SPEND"
  }

  # Optional: forecast-based alerts
  threshold_rules {
    threshold_percent = 1.0
    spend_basis       = "FORECASTED_SPEND"
  }

  all_updates_rule {
    monitoring_notification_channels = [
      google_monitoring_notification_channel.email[0].name
    ]
    disable_default_iam_recipients = true
  }

  depends_on = [google_monitoring_notification_channel.email]
}

# Cost monitoring metrics
resource "google_monitoring_alert_policy" "high_cost_spike" {
  count = var.enable_budget_alerts && var.enable_vertex_ai_alerts ? 1 : 0

  display_name = "Cost Spike Alert - ${var.environment}"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "Vertex AI Cost Spike"
    condition_threshold {
      filter     = "resource.type = \"aiplatform.googleapis.com/Endpoint\" AND metric.type = \"billing/monthly_cost\""
      duration   = "3600s" # 1 hour
      comparison = "COMPARISON_GT"

      # Alert if hourly cost exceeds $5 (adjust as needed)
      threshold_value = var.cost_alert_threshold

      aggregations {
        alignment_period   = "3600s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email[0].name]
}

# Resource utilization monitoring
resource "google_monitoring_alert_policy" "resource_usage" {
  count = var.enable_vertex_ai_alerts ? 1 : 0

  display_name = "Resource Usage Alert - ${var.environment}"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "High CPU Utilization"
    condition_threshold {
      filter          = "resource.type = \"aiplatform.googleapis.com/Endpoint\" AND metric.type = \"compute.googleapis.com/instance/cpu/utilization\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8 # 80% CPU utilization

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MEAN"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email[0].name]
}
