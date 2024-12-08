output "raw_data_bucket" {
  description = "The name of the raw data bucket"
  value       = google_storage_bucket.raw_data.name
}

output "landmarks_bucket" {
  description = "The name of the landmarks data bucket"
  value       = google_storage_bucket.landmarks.name
}

output "training_data_bucket" {
  description = "The name of the training data bucket"
  value       = google_storage_bucket.training_data.name
}

output "models_bucket" {
  description = "The name of the models bucket"
  value       = google_storage_bucket.models.name
}

output "staging_bucket" {
  description = "The name of the Vertex AI staging bucket"
  value       = google_storage_bucket.staging.name
}
