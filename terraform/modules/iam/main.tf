# Service account for ML training jobs
resource "google_service_account" "ml_training" {
  account_id   = "ml-training-${var.environment}"
  display_name = "ML Training Service Account ${var.environment}"
  project      = var.project_id
}

# Service account for Cloud Run
resource "google_service_account" "cloud_run" {
  account_id   = "cloud-run-${var.environment}"
  display_name = "Cloud Run Service Account ${var.environment}"
  project      = var.project_id
}

# Grant storage access to service account
resource "google_project_iam_member" "storage_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.ml_training.email}"
}

# Additional roles for ML training
resource "google_project_iam_member" "ml_training_roles" {
  for_each = toset([
    "roles/ml.developer",
    "roles/storage.objectViewer"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.ml_training.email}"
}

# Cloud Run service account roles
resource "google_project_iam_member" "cloud_run_roles" {
  for_each = toset([
    "roles/storage.objectViewer",    # Access to storage buckets
    "roles/artifactregistry.reader", # Pull images from Artifact Registry
    "roles/cloudtrace.agent",        # Write cloud trace data
    "roles/monitoring.metricWriter"  # Write monitoring metrics
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# Allow project members to invoke Cloud Run
resource "google_cloud_run_service_iam_member" "project_access" {
  project  = var.project_id
  location = var.region
  service  = var.cloud_run_service_name
  role     = "roles/run.invoker"
  member   = "projectViewer" # Allows all project members with at least viewer role to invoke
}

# resource "google_cloud_run_service_iam_member" "public_access" {
#   project  = var.project_id
#   location = var.region
#   service  = var.cloud_run_service_name
#   role     = "roles/run.invoker"
#   member   = "allUsers"
# }

# Output the service account emails
output "ml_training_service_account" {
  value = google_service_account.ml_training.email
}

output "cloud_run_service_account" {
  value = google_service_account.cloud_run.email
}
