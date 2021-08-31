# 'Constants'
locals {
  output_path = "${path.module}/.files/init.zip"
}

variable "lambda_name" {
  type    = string
  default = "docdb-autoscaling"
}
