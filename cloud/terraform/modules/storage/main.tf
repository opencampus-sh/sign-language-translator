# Training data bucket
resource "google_storage_bucket" "training_data" {
  name          = "${var.project_id}-training-data-${var.environment}"
  location      = "EU"
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  labels = {
    environment = var.environment
    purpose     = "training-data"
  }
}
