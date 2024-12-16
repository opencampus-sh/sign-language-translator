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

# Create GitHub connection
resource "google_cloudbuildv2_connection" "github_connection" {
  project  = var.project_id
  location = var.region
  name     = "${var.environment}-github-connection"

  github_config {
    app_installation_id = var.github_app_installation_id
    authorizer_credential {
      oauth_token_secret_version = var.github_token_secret_version
    }
  }
}

resource "google_cloudbuildv2_repository" "github_repo" {
  project           = var.project_id
  location          = var.region
  name              = var.github_repo
  parent_connection = google_cloudbuildv2_connection.github_connection.name
  remote_uri        = "https://github.com/${var.github_owner}/${var.github_repo}.git"
}

# Manual trigger (can be executed via gcloud)
resource "google_cloudbuild_trigger" "model_deployment_manual" {
  name = "${var.environment}-${var.endpoint_name}-deploy"

  source_to_build {
    repository = google_cloudbuildv2_repository.github_repo.id
    ref        = "refs/heads/main"
    repo_type  = "GITHUB"
  }

  git_file_source {
    path      = "models/types/huggingface/cloud-build/cloudbuild.yaml"
    uri       = "https://github.com/${var.github_owner}/${var.github_repo}"
    repo_type = "GITHUB"
  }

  substitutions = {
    _ENVIRONMENT   = var.environment
    _MODEL_ID      = var.model_id
    _MODEL_VERSION = var.model_version
    _HF_TASK       = var.hf_task
    _REGION        = var.region
    _ENDPOINT      = google_vertex_ai_endpoint.model_endpoint.name
    _HF_TOKEN      = var.huggingface_token
  }
}


# Add Cloud Build triggers for model deployment
# Automatic trigger on main branch pushes
# resource "google_cloudbuild_trigger" "model_deployment_auto" {
#   name        = "${var.environment}-${var.endpoint_name}-deploy-auto"
#   description = "Automatic trigger for model deployment on main branch pushes"
#   location    = var.region
#   project     = var.project_id

#   github {
#     owner = var.github_owner
#     name  = var.github_repo
#     push {
#       branch = "^main$"
#     }
#   }

#   included_files = [
#     "models/types/huggingface/**"
#   ]

#   filename = "models/types/huggingface/cloud-build/cloudbuild.yaml"

#   substitutions = {
#     _ENVIRONMENT = var.environment
#     _MODEL_ID    = var.model_id
#     _MODEL_VERSION = var.model_version
#     _HF_TASK     = var.hf_task
#     _REGION      = var.region
#     _ENDPOINT    = google_vertex_ai_endpoint.model_endpoint.name
#   }
# }
# Create GitHub connection
