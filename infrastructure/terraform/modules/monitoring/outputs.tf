output "notification_channel_id" {
  description = "The ID of the notification channel"
  value       = var.notification_email != null ? google_monitoring_notification_channel.email[0].name : null
}

output "latency_alert_policy_id" {
  description = "The ID of the latency alert policy"
  value       = try(google_monitoring_alert_policy.vertex_ai_latency[0].name, null)
}

output "error_alert_policy_id" {
  description = "The ID of the error rate alert policy"
  value       = try(google_monitoring_alert_policy.vertex_ai_errors[0].name, null)
}

output "cost_alert_policy_id" {
  description = "The ID of the cost spike alert policy"
  value       = try(google_monitoring_alert_policy.high_cost_spike[0].name, null)
}

output "resource_usage_alert_policy_id" {
  description = "The ID of the resource usage alert policy"
  value       = try(google_monitoring_alert_policy.resource_usage[0].name, null)
}
