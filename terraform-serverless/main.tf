terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 3.53"
    }
  }
}

provider "google" {
  project = var.project
}

locals {
  function_folder = "function"
  function_name   = "processing"

  service_folder = "service"
  service_name   = "cats"

  bucket_folder = "media"
  bucket_name   = "${var.project}-media"

  deployment_name = "cats"
  cats_worker_sa  = "serviceAccount:${google_service_account.cats_worker.email}"
}
