# 'Constants'
locals {
  region = data.aws_region.current.name
  output_path = "${path.module}/.files/init.zip"
}

variable "name" {
  type    = string
  default = "docdb-autoscaling"
}
