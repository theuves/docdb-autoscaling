# SNS topic (trigged by CloudWathc)
resource "aws_sns_topic" "main" {
  name = var.name
}
