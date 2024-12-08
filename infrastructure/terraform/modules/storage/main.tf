# Training data bucket
resource "google_storage_bucket" "training_data" {
  name          = "${var.project_id}-${var.environment}-training-data"
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

  labels = {
    environment = var.environment
    purpose     = "training-data"
  }
}

# Raw data bucket
resource "google_storage_bucket" "raw_data" {
  name          = "${var.project_id}-${var.environment}-raw-data"
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

  labels = {
    environment = var.environment
    purpose     = "raw-data"
  }
}

# Landmarks data bucket
resource "google_storage_bucket" "landmarks" {
  name          = "${var.project_id}-${var.environment}-landmarks"
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

  labels = {
    environment = var.environment
    purpose     = "landmarks"
  }
}

# Models bucket
resource "google_storage_bucket" "models" {
  name          = "${var.project_id}-${var.environment}-models"
  location      = var.region
  force_destroy = var.environment != "prod"
  project       = var.project_id

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 90 # Longer retention for model artifacts
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  labels = {
    environment = var.environment
    purpose     = "models"
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
