provider "google" {
  project = var.project_id
  region  = var.region
}

module "project" {
  source     = "../../modules/project"
  project_id = var.project_id
}

module "storage" {
  source      = "../../modules/storage"
  project_id  = var.project_id
  region      = var.region
  environment = "dev"
  depends_on  = [module.project]
}

module "iam" {
  source      = "../../modules/iam"
  project_id  = var.project_id
  environment = "dev"
  region      = var.region

  depends_on = [
    module.project,
    module.vertex_ai
  ]
}

module "vertex_ai" {
  source = "../../modules/vertex_ai"

  project_id    = var.project_id
  environment   = "dev"
  region        = var.region
  model_version = var.model_version
  model_path    = "gs://${module.storage.training_data_bucket}/${var.model_version}"

  # Development-specific configurations
  machine_type        = "n1-standard-2"
  min_replicas        = 1
  max_replicas        = 1
  accelerator_type    = null # No GPU for dev
  accelerator_count   = 0
  container_image_uri = "europe-docker.pkg.dev/vertex-ai/prediction/pytorch-cpu.1-13:latest"

  depends_on = [
    module.project,
    module.storage
  ]
}

module "monitoring" {
  source = "../../modules/monitoring"

  project_id  = var.project_id
  environment = "dev"

  # Monitor Vertex AI endpoint
  vertex_ai_endpoint_id = module.vertex_ai.endpoint_id
  vertex_ai_model_id    = module.vertex_ai.model_id

  # Basic alerts for development
  alert_thresholds = {
    latency_threshold    = 1000 # 1 second
    error_rate_threshold = 0.05 # 5% error rate
  }

  notification_email = var.notification_email # Optional for dev, but good for debugging

  depends_on = [module.project, module.vertex_ai]
}
