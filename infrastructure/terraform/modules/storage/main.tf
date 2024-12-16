# Main data bucket with subfolders
resource "google_storage_bucket" "data" {
  name          = "${var.project_id}-${var.environment}-data"
  location      = var.region
  force_destroy = var.environment != "prod"
  project       = var.project_id

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  # Special rule for models subfolder
  lifecycle_rule {
    condition {
      age            = 90 # Longer retention for model artifacts
      matches_prefix = ["models/"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  labels = {
    environment = var.environment
    purpose     = "data"
  }
}

# Vertex AI staging bucket
resource "google_storage_bucket" "staging" {
  name          = "${var.project_id}-${var.environment}-staging"
  location      = var.region
  force_destroy = true # Staging data can always be recreated
  project       = var.project_id

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1 # Clean up staging data after 1 day
    }
    action {
      type = "Delete"
    }
  }

  labels = {
    environment = var.environment
    purpose     = "staging"
  }
}
