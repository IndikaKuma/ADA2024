variable "project_id" {
  description = "The ID of the project in which to provision resources."
  type        = string
}

variable "function_location" {
  description = "The location of this cloud function"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Name of the bucket to store the function code"
  type        = string
}

variable "function_source_location" {
  description = "path to the original source code of the function"
  type        = string
}

variable "function_source_zip" {
  description = "Name of the zip file containing the function code"
  type        = string
}

