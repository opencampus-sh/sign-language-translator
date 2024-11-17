# Model registry configuration
resource "google_vertex_ai_model" "translator_model" {
  name         = "sign-language-translator-${var.environment}"
  display_name = "sign-language-translator-${var.environment}"
  artifact_uri = "gs://${google_storage_bucket.model_artifacts.name}/${var.model_version}"
  project      = var.project_id
  region       = var.region

  container_spec {
    image_uri = var.container_image_uri
    env {
      name  = "MODEL_PATH"
      value = var.model_path
    }
  }
  depends_on = [google_project_service.vertex_ai]
}

# Endpoint configuration
resource "google_vertex_ai_endpoint" "translator_endpoint" {
  name         = "translator-endpoint-${var.environment}"
  display_name = "sign-language-translator-${var.environment}"
  location     = var.region
  project      = var.project_id
  description  = "Endpoint for sign language translation model"

  depends_on = [google_project_service.vertex_ai]
}

# Model deployment
resource "google_vertex_ai_model_deployment" "translator_deployment" {
  name         = "translator-deployment-${var.environment}-${var.model_version}"
  model        = google_vertex_ai_model.translator_model.id
  endpoint     = google_vertex_ai_endpoint.translator_endpoint.id
  display_name = "sign-language-translator-${var.environment}-${var.model_version}"
  location     = var.region
  project      = var.project_id

  dedicated_resources {
    machine_spec {
      machine_type      = var.machine_type
      accelerator_type  = var.accelerator_type
      accelerator_count = var.accelerator_count
    }
    min_replica_count = var.min_replicas
    max_replica_count = var.max_replicas
  }

  traffic_split = {
    "0" = 100
  }
}
