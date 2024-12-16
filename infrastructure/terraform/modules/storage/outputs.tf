output "data_bucket" {
  description = "The name of the main data bucket"
  value       = google_storage_bucket.data.name
}

output "staging_bucket" {
  description = "The name of the Vertex AI staging bucket"
  value       = google_storage_bucket.staging.name
}
