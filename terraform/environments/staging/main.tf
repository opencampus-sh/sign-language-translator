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
  # Add these required parameters
  region                 = var.region
  cloud_run_service_name = module.cloudrun.service_name

  depends_on = [
    module.project,
    module.cloudrun
  ]
}

module "monitoring" {
  source = "../../modules/monitoring"

  project_id  = var.project_id
  environment = "dev"
  storage_buckets = [
    module.storage.training_data_bucket,
  ]
  notification_email = var.notification_email
  depends_on         = [module.project]
}

module "vertex_ai" {
  source = "../../modules/vertex_ai"

  project_id    = var.project_id
  environment   = "staging"
  region        = var.region
  model_version = var.model_version
  model_path    = "gs://${module.storage.training_data_bucket}/${var.model_version}"

  # Staging-specific configurations
  machine_type        = "n1-standard-4"
  min_replicas        = 1
  max_replicas        = 2
  accelerator_type    = "NVIDIA_TESLA_T4"
  accelerator_count   = 1
  container_image_uri = "europe-docker.pkg.dev/vertex-ai/prediction/pytorch-gpu.1-13:latest"
}


# module "cloudrun" {
#   source          = "../../modules/cloudrun"
#   project_id      = var.project_id
#   region          = var.region
#   environment     = "dev"
#   repository_name = "sign-language-translator" # Should match your Artifact Registry repository name

#   service_name = "sign-language-translator"
#   memory_limit = "2Gi"
#   cpu_limit    = "1000m"
#   github_owner = var.github_owner
#   branch_name  = var.branch_name

#   depends_on = [
#     module.project,
#     module.iam,
#     module.storage
#   ]
# }