# infrastructure/terraform/modules/vertex_ai/outputs.tf

output "endpoint_id" {
  description = "The ID of the created Vertex AI endpoint"
  value       = google_vertex_ai_endpoint.model_endpoint.name
}

output "endpoint_resource_name" {
  description = "The full resource name of the Vertex AI endpoint"
  value       = google_vertex_ai_endpoint.model_endpoint.id
}

output "artifact_registry_repository" {
  description = "The name of the Artifact Registry repository"
  value       = google_artifact_registry_repository.model_repo.name
}

output "model_artifacts_bucket" {
  description = "The name of the GCS bucket for model artifacts"
  value       = google_storage_bucket.model_artifacts.name
}
