data "archive_file" "cloud-function-zip" {
  type        = "zip"
  output_path = var.function_source_zip
  source_dir  = "${path.module}/${var.function_source_location}"
}

resource "google_storage_bucket" "bucket" {
  name                        = var.bucket_name
  location                    = "US"
  uniform_bucket_level_access = true
  project                     = var.project_id
}

resource "google_storage_bucket_object" "function-source" {
  name   = var.function_source_zip
  bucket = google_storage_bucket.bucket.name
  source = var.function_source_zip
}