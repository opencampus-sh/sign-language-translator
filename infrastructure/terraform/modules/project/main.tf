# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "iam.googleapis.com",
    "monitoring.googleapis.com",
    "billingbudgets.googleapis.com",
    "aiplatform.googleapis.com",
    "servicenetworking.googleapis.com",
    "secretmanager.googleapis.com"
  ])

  project = var.project_id
  service = each.key

  disable_dependent_services = false
  disable_on_destroy         = false

  # Add a timeout to ensure the API is fully enabled
  timeouts {
    create = "30m"
    update = "30m"
  }
}
