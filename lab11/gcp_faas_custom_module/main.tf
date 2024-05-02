provider "google" {
  project     = var.project_id
  region      = "us-central1"
  zone        = "us-central1-c"
}

module "zip-upload-gcs" {
  source = "./modules/zip-upload-gcs"

  bucket_name = var.bucket_name
  function_source_location = var.function_source_location
  function_source_zip = var.function_source_zip
  project_id = var.project_id
}

module "cloud_functions2" {
  source  = "GoogleCloudPlatform/cloud-functions/google"
  version = "~> 0.4"

  project_id        = var.project_id
  function_name     = "cal-http"
  function_location = var.function_location
  runtime           = "python310"
  entrypoint        = "cal_http"
  storage_source = {
    bucket     = var.bucket_name
    object     =  module.zip-upload-gcs.function-zip-uploaded
    generation = null
  }
}