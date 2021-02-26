# Enable services
resource "google_project_service" "vision" {
  service = "vision.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "run" {
  service = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam" {
  service = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild" {
  service = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudfunctions" {
  service = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

# Create a service account
resource "google_service_account" "cats_worker" {
  account_id   = "cats-worker"
  display_name = "Cats Worker SA"
}

# Set permissions
resource "google_project_iam_binding" "service_permissions" {
  for_each = toset([
    "run.invoker", "cloudfunctions.invoker"
  ])

  role       = "roles/${each.key}"
  members    = [local.cats_worker_sa]
  depends_on = [google_service_account.cats_worker]
}
