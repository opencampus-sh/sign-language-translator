output "github_token_secret_version" {
  description = "The resource name of the GitHub token secret version"
  value       = "${google_secret_manager_secret.github_token.id}/versions/latest"
}

output "vertex_ai_service_account" {
  description = "The email of the Vertex AI service account"
  value       = google_service_account.vertex_ai.email
}

output "ml_training_service_account" {
  description = "The email of the ML training service account"
  value       = google_service_account.ml_training.email
}

output "cloud_run_service_account" {
  description = "The email of the Cloud Run service account"
  value       = google_service_account.cloud_run.email
}
