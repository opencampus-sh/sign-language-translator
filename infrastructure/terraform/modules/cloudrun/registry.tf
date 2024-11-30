# terraform/modules/cloudrun/registry.tf
resource "google_artifact_registry_repository" "translator" {
  provider      = google
  location      = var.region
  repository_id = "translator-${var.environment}"
  description   = "Docker repository for sign language translator images"
  format        = "DOCKER"
}

# Optional: Configure registry cleanup policy
resource "google_artifact_registry_repository_cleanup_policy" "cleanup" {
  provider   = google
  location   = var.region
  repository = google_artifact_registry_repository.translator.name
  project    = var.project_id

  condition {
    tag_state    = "TAGGED"
    older_than   = "2592000s" # 30 days
    tag_prefixes = ["dev"]    # Only clean up dev tags
  }

  action {
    type = "DELETE"
  }
}
