resource "aws_lambda_function" "job_tracker_api" {
  function_name = "job-tracker-api"

  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  role = aws_iam_role.lambda_role.arn

  handler = "app.main.handler"
  runtime = "python3.11"

  timeout     = 10
  memory_size = 128

  environment {
    variables = {
      AWS_REGION_NAME = "eu-west-2"
    }
  }

  depends_on = [
    aws_iam_role_policy.lambda_policy
  ]
}