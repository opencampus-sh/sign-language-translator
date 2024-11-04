output "repository_url" {
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.translator.repository_id}"
  description = "URL of the Artifact Registry repository"
}

output "repository_id" {
  value       = google_artifact_registry_repository.translator.repository_id
  description = "ID of the Artifact Registry repository"
}

output "service_url" {
  value       = google_cloud_run_service.translator_service.status[0].url
  description = "URL of the deployed Cloud Run service"
}

output "repository_url" {
  value       = google_artifact_registry_repository.translator_repo.name
  description = "URL of the Artifact Registry repository"
}
