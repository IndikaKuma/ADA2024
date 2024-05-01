variable "project_id" {
  type = string
}

variable "ada_github_uri" {
  type = string
  default = "https://github.com/IndikaKuma/ADA2024.git"
}

variable "gce_ssh_user" {
  type = string
}

variable "gce_ssh_pub_key_file" {
  type = string
}

variable "gce_ssh_pri_key_file" {
  type = string
}