# Lambda function
resource "aws_lambda_function" "main" {
  filename         = local.output_path
  function_name    = var.name
  role             = aws_iam_role.lambda.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.source_code.output_base64sha256
  runtime          = "python3.9"

  # Wait for the .zip file 
  depends_on = [
    data.archive_file.source_code
  ]
}
