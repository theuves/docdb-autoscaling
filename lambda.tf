# Lambda function
resource "aws_lambda_function" "main" {
  filename         = local.output_path
  function_name    = var.name
  role             = aws_iam_role.lambda.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.source_code.output_base64sha256
  runtime          = "python3.9"

  environment {
    variables = {
      min_capacity       = tostring(var.min_capacity)
      max_capacity       = tostring(var.max_capacity)
      cluster_identifier = var.cluster_identifier
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.main,
    data.archive_file.source_code
  ]
}

resource "aws_lambda_permission" "sns" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.arn
  principal     = "sns.amazonaws.com"
  statement_id  = "AllowSubscriptionToSNS"
  source_arn    = aws_sns_topic.main.arn
}