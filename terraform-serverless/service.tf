# The Cloud Run service
resource "google_cloud_run_service" "cats" {
  name                       = local.service_name
  location                   = var.region
  autogenerate_revision_name = true

  template {
    spec {
      service_account_name = google_service_account.cats_worker.email
      containers {
        image = data.external.image_digest.result.image
        env {
          name  = "BUCKET_NAME"
          value = google_storage_bucket.media.name
        }
        env {
          name  = "FUNCTION_NAME"
          value = google_cloudfunctions_function.function.https_trigger_url
        }
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.run]
}

# Set service public
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.cats.location
  project  = google_cloud_run_service.cats.project
  service  = google_cloud_run_service.cats.name

  policy_data = data.google_iam_policy.noauth.policy_data
  depends_on  = [google_cloud_run_service.cats]
}


# WORKAROUND 
data "external" "image_digest" {
  program = ["bash", "scripts/get_latest_tag.sh", var.project, local.service_name]
}
# END WORKAROUND