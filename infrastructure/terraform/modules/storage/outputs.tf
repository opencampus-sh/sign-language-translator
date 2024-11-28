output "training_data_bucket" {
  description = "The name of the training data bucket"
  value       = google_storage_bucket.training_data.name
}
