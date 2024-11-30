# infrastructure/terraform/modules/vertex_ai/main.tf

# Get project details
data "google_project" "current" {
  project_id = var.project_id
}

# Vertex AI endpoint
resource "google_vertex_ai_endpoint" "model_endpoint" {
  name         = "${var.environment}-${var.endpoint_name}-endpoint"
  display_name = "${var.environment} ${var.endpoint_name} Endpoint"
  description  = "Endpoint for ${var.endpoint_name} model in ${var.environment}"
  location     = var.region
  project      = var.project_id
}

# Bucket for model artifacts
resource "google_storage_bucket" "model_artifacts" {
  name          = "${var.project_id}-${var.environment}-${var.endpoint_name}-artifacts"
  location      = var.region
  force_destroy = var.environment != "prod"
  project       = var.project_id

  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

# Bucket for batch jobs
resource "google_storage_bucket" "batch_jobs" {
  name          = "${var.project_id}-${var.environment}-batch-jobs"
  location      = var.region
  force_destroy = var.environment != "prod"
  project       = var.project_id

  uniform_bucket_level_access = true
}

# Artifact Registry repository for model container images
resource "google_artifact_registry_repository" "model_repo" {
  location      = var.region
  repository_id = "${var.environment}-${var.endpoint_name}-repo"
  description   = "Docker repository for ${var.endpoint_name} model containers"
  format        = "DOCKER"
  project       = var.project_id
}

# Artifact Registry repository for batch jobs
resource "google_artifact_registry_repository" "batch_jobs_repo" {
  location      = var.region
  repository_id = "${var.environment}-batch-jobs"
  description   = "Docker repository for ML batch job containers"
  format        = "DOCKER"
  project       = var.project_id
}

# IAM binding for Vertex AI service account to access model artifacts
resource "google_storage_bucket_iam_member" "vertex_ai_bucket_access" {
  bucket = google_storage_bucket.model_artifacts.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.service_account_email}"

  # Add a lifecycle block to handle empty service account email
  lifecycle {
    precondition {
      condition     = var.service_account_email != ""
      error_message = "service_account_email must not be empty"
    }
  }
}
