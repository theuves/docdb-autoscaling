# SNS topic (trigged by CloudWathc)
resource "aws_sns_topic" "main" {
  name = var.name
}

# Call AWS Lambda when publish messages
resource "aws_sns_topic_subscription" "main" {
  topic_arn = aws_sns_topic.main.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.main.arn
}