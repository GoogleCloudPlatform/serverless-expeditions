# The Cloud Function
resource "google_cloudfunctions_function" "function" {
  name        = local.function_name
  description = "processing"
  runtime     = "python37"
  region      = var.region

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.source.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "detect_cat"
  service_account_email = google_service_account.cats_worker.email

  depends_on = [google_project_service.cloudfunctions]
}

# A dedicated Cloud Storage bucket to store the zip source
resource "google_storage_bucket" "source" {
  name = "${var.project}-source"
}

# Create a fresh archive of the current function folder
data "archive_file" "function" {
  type        = "zip"
  output_path = "temp/function_code_${timestamp()}.zip"
  source_dir  = local.function_folder
}

# The archive in Cloud Stoage uses the md5 of the zip file
# This ensures the Function is redeployed only when the source is changed.
resource "google_storage_bucket_object" "archive" {
  name = "${local.function_folder}_${data.archive_file.function.output_md5}.zip" # will delete old items

  bucket = google_storage_bucket.source.name
  source = data.archive_file.function.output_path

  depends_on = [data.archive_file.function]
}
