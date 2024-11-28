# terraform/modules/cloudrun/main.tf
# Cloud Run service
resource "google_cloud_run_service" "translator_service" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        # Update the image reference to use the correct resource
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.translator.repository_id}/${var.service_name}:${var.image_tag}"

        resources {
          limits = {
            cpu    = var.cpu_limit
            memory = var.memory_limit
          }
        }

        env {
          name  = "PROJECT_ID"
          value = var.project_id
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "run.googleapis.com/client-name"   = "terraform"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_artifact_registry_repository.translator]
}

# IAM binding for invoking the service
resource "google_cloud_run_service_iam_member" "public_invoker" {
  service  = google_cloud_run_service.translator_service.name
  location = google_cloud_run_service.translator_service.location
  role     = "roles/run.invoker"
  member   = var.invoker_member
}
