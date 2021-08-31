# IAM role for AWS Lambda
resource "aws_iam_role" "lambda" {
  name = "${var.name}-${local.region}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}

# IAM policy for AWS Lambda
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = jsonencode({
    Version: "2012-10-17",
    Statement: [
      {
        Action: [
          "logs:CreateLogStream",
          "logs:CreateLogGroup"
        ],
        Resource: "${aws_cloudwatch_log_group.main.arn}:*",
        Effect: "Allow"
      },
      {
        Action: [
          "logs:PutLogEvents"
        ],
        Resource: "${aws_cloudwatch_log_group.main.arn}:*:*",
        Effect: "Allow"
      }
    ]
  })
}