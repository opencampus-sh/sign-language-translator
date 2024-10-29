provider "google" {
  project = var.project_id
  region  = var.region
}

module "storage" {
  source      = "../../modules/storage"
  project_id  = var.project_id
  region      = var.region
  environment = "dev"
}

module "iam" {
  source      = "../../modules/iam"
  project_id  = var.project_id
  environment = "dev"
}

module "monitoring" {
  source = "../../modules/monitoring"
  
  project_id    = var.project_id
  environment   = "dev"
  storage_buckets = [
    module.storage.training_data_bucket,
  ]
  notification_email = var.notification_email
}
