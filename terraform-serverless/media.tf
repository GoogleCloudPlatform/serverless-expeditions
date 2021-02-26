resource "google_storage_bucket" "media" {
  name = local.bucket_name
}

resource "google_storage_bucket_object" "cats" {
  for_each = fileset("${path.module}/${local.bucket_folder}", "*")

  name   = each.value
  source = "${path.module}/${local.bucket_folder}/${each.value}"
  bucket = google_storage_bucket.media.name
}

resource "google_storage_bucket_iam_policy" "media" {
  bucket = google_storage_bucket.media.name

  # Generated with assistance from terraformer
  policy_data = <<POLICY
{
  "bindings": [
    {
      "members": [
        "projectEditor:${var.project}",
        "projectOwner:${var.project}"
      ],
      "role": "roles/storage.legacyBucketOwner"
    },
    {
      "members": [
        "projectViewer:${var.project}",
        "${local.cats_worker_sa}"
      ],
      "role": "roles/storage.legacyBucketReader"
    },
    {
      "members": [
        "projectViewer:${var.project}",
        "${local.cats_worker_sa}"
      ],
      "role": "roles/storage.legacyObjectReader"
    }
  ]
}
POLICY
}