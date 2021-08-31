# 'Constants'
locals {
  region      = data.aws_region.current.name
  output_path = "${path.module}/.files/init.zip"
}

variable "cluster_identifier" {
  type        = string
  description = "DocumentDB cluster identifier."
}

variable "name" {
  type        = string
  default     = "docdb-autoscaling"
  description = "Resources name."
}

variable "min_capacity" {
  type        = number
  default     = 0
  description = "The minimum capacity."

  # Idiot-proof
  validation {
    condition     = var.min_capacity >= 0
    error_message = "Minimum capacity cannot be lower than 0."
  }

  # Source: https://docs.aws.amazon.com/documentdb/latest/developerguide/how-it-works.html
  validation {
    condition     = var.min_capacity <= 15
    error_message = "DocumentDB does not allow more than 15 replica instances."
  }
}

variable "max_capacity" {
  type        = number
  default     = 15
  description = "The maximum capacity."

  # Source: https://docs.aws.amazon.com/documentdb/latest/developerguide/how-it-works.html
  validation {
    condition     = var.max_capacity <= 15
    error_message = "DocumentDB does not allow more than 15 replica instances."
  }
}

variable "scaling_policy" {
  type = list(object({
    metric_name = string
    target      = number
    statistic   = string
    cooldown    = number
    action      = string
  }))
  default = [
    {
      metric_name = "CPUUtilization"
      target      = 60
      statistic   = "Average"
      cooldown    = 120
      action      = "scale-out"
    },
    {
      metric_name = "CPUUtilization"
      target      = 60
      statistic   = "Average"
      cooldown    = 120
      action      = "scale-in"
    }
  ]
}
