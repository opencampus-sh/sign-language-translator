terraform {
  required_version = ">= 1.0.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.12.0"
    }
  }

  backend "gcs" {
    bucket = "sign-lang-translator-tfstate"
    prefix = "terraform/state"
  }
}
