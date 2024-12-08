# Service accounts
data "google_project" "current" {
  project_id = var.project_id
}

resource "time_sleep" "wait_for_secret_manager" {
  depends_on = [data.google_project.current]

  # Wait for 60 seconds for API activation to propagate
  create_duration = "60s"
}

resource "google_service_account" "cloud_run" {
  account_id   = "cloud-run-${var.environment}"
  display_name = "Cloud Run Service Account ${var.environment}"
  project      = var.project_id
}

resource "google_service_account" "ml_training" {
  account_id   = "ml-training-${var.environment}"
  display_name = "ML Training Service Account ${var.environment}"
  project      = var.project_id
}

resource "google_service_account" "vertex_ai" {
  account_id   = "vertex-ai-${var.environment}"
  display_name = "Vertex AI Service Account ${var.environment}"
  project      = var.project_id
}

resource "google_service_account" "batch_jobs" {
  account_id   = "batch-jobs-${var.environment}"
  display_name = "ML Batch Jobs Service Account ${var.environment}"
  project      = var.project_id
}

# ML Training roles
resource "google_project_iam_member" "ml_training_roles" {
  for_each = toset([
    "roles/ml.developer",
    "roles/storage.objectViewer"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.ml_training.email}"
}

# Vertex AI roles
resource "google_project_iam_member" "vertex_ai_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.admin",
    "roles/artifactregistry.writer",
    "roles/monitoring.metricWriter",
    "roles/logging.logWriter"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.vertex_ai.email}"
}

# Batch jobs roles
resource "google_project_iam_member" "batch_jobs_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.objectViewer",
    "roles/storage.objectCreator",
    "roles/artifactregistry.reader",
    "roles/monitoring.metricWriter"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.batch_jobs.email}"
}

# Cloud Run roles
resource "google_project_iam_member" "cloud_run_roles" {
  for_each = toset([
    "roles/storage.objectViewer",
    "roles/artifactregistry.reader",
    "roles/cloudtrace.agent",
    "roles/monitoring.metricWriter"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# Cloud Run public access (conditional)
resource "google_cloud_run_service_iam_member" "project_access" {
  count = var.enable_cloud_run_iam ? 1 : 0

  project  = var.project_id
  location = var.region
  service  = "sign-language-translator"
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloud Build IAM roles
resource "google_project_iam_member" "cloudbuild_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.admin",
    "roles/artifactregistry.writer"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${data.google_project.current.number}@cloudbuild.gserviceaccount.com"
}

# Create Secret for GitHub token
resource "google_secret_manager_secret" "github_token" {
  secret_id = "${var.environment}-github-token"
  project   = var.project_id

  replication {
    auto {}
  }
}

# Create the secret version as a separate resource
resource "google_secret_manager_secret_version" "github_token" {
  secret      = google_secret_manager_secret.github_token.id
  secret_data = var.github_token

  depends_on = [
    google_secret_manager_secret.github_token,
    time_sleep.wait_for_secret_manager
  ]
}

# Update the IAM binding to use the specific version
resource "google_secret_manager_secret_iam_member" "cloudbuild_service_account_access" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.github_token.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:service-${data.google_project.current.number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"

  depends_on = [
    google_secret_manager_secret.github_token,
    google_secret_manager_secret_version.github_token,
    time_sleep.wait_for_secret_manager
  ]
}
