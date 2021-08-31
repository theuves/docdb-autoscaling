# Create a .zip file with the Python source code
data "archive_file" "source_code" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = local.output_path
}

# Get current region
data "aws_region" "current" {}