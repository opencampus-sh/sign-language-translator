output "ml_training_service_account" {
  description = "The email of the ML training service account"
  value       = google_service_account.ml_training.email
}
