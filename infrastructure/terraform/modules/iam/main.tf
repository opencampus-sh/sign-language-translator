# Service accounts
resource "google_service_account" "ml_training" {
  account_id   = "ml-training-${var.environment}"
  display_name = "ML Training Service Account ${var.environment}"
  project      = var.project_id
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
    "roles/storage.objectViewer",
    "roles/artifactregistry.reader",
    "roles/monitoring.metricWriter" # For model monitoring
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.vertex_ai.email}"
}

# Batch jobs roles
resource "google_project_iam_member" "batch_jobs_roles" {
  for_each = toset([
    "roles/aiplatform.customJobUser",
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
