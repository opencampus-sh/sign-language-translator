resource "google_cloudbuild_trigger" "translator_build" {
  name     = "${var.service_name}-${var.environment}"
  location = var.region

  github {
    owner = var.github_owner # Use the variable here instead of hardcoded value
    name  = "sign-language-translator"
    push {
      branch = var.branch_name
    }
  }

  filename = "build/cloudbuild.yaml"

  substitutions = {
    _REGION          = var.region
    _SERVICE_NAME    = var.service_name
    _SERVICE_ACCOUNT = google_service_account.cloud_run.email
  }
}
