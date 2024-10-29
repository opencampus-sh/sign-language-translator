# Service account for ML training jobs
resource "google_service_account" "ml_training" {
  account_id   = "ml-training-${var.environment}"
  display_name = "ML Training Service Account ${var.environment}"
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
