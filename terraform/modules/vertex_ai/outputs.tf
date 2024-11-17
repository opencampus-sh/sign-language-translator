output "endpoint_id" {
  description = "The ID of the Vertex AI endpoint"
  value       = google_vertex_ai_endpoint.translator_endpoint.id
}

output "endpoint_name" {
  description = "The name of the Vertex AI endpoint"
  value       = google_vertex_ai_endpoint.translator_endpoint.name
}

output "endpoint_display_name" {
  description = "The display name of the Vertex AI endpoint"
  value       = google_vertex_ai_endpoint.translator_endpoint.display_name
}

output "model_id" {
  description = "The ID of the deployed model"
  value       = google_vertex_ai_model.translator_model.id
}

output "model_name" {
  description = "The name of the deployed model"
  value       = google_vertex_ai_model.translator_model.name
}

output "model_version" {
  description = "The version of the deployed model"
  value       = var.model_version
}

output "deployment_id" {
  description = "The ID of the model deployment"
  value       = google_vertex_ai_model_deployment.translator_deployment.id
}

output "deployment_state" {
  description = "The state of the model deployment"
  value       = google_vertex_ai_model_deployment.translator_deployment.deployment_state
}

output "artifact_uri" {
  description = "The GCS URI where the model artifacts are stored"
  value       = google_vertex_ai_model.translator_model.artifact_uri
}

output "resource_usage" {
  description = "Resource configuration of the deployment"
  value = {
    machine_type      = var.machine_type
    min_replicas      = var.min_replicas
    max_replicas      = var.max_replicas
    accelerator_type  = var.accelerator_type
    accelerator_count = var.accelerator_count
  }
}

output "endpoint_uri" {
  description = "The URI of the endpoint for making predictions"
  value       = "${var.region}-aiplatform.googleapis.com/${google_vertex_ai_endpoint.translator_endpoint.name}"
}

output "model_artifacts_bucket" {
  description = "The name of the GCS bucket containing model artifacts"
  value       = google_storage_bucket.model_artifacts.name
} 
