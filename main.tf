locals {
  output_path = "${path.module}/.files/init.zip"
}

data "archive_file" "source_code" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = local.output_path
}

resource "aws_iam_role" "lambda" {
  name = "${var.lambda_name}-role"

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

resource "aws_lambda_function" "main" {
  filename         = local.output_path
  function_name    = var.lambda_name
  role             = aws_iam_role.lambda.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.source_code.output_base64sha256
  runtime          = "python3.9"

  depends_on = [
    data.archive_file.source_code
  ]
}
