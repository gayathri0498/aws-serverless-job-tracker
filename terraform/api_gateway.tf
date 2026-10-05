resource "aws_apigatewayv2_api" "job_tracker_api" {
  name          = "job-tracker-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id = aws_apigatewayv2_api.job_tracker_api.id

  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.job_tracker_api.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default_route" {
  api_id = aws_apigatewayv2_api.job_tracker_api.id

  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default_stage" {
  api_id = aws_apigatewayv2_api.job_tracker_api.id

  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.job_tracker_api.function_name

  principal  = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.job_tracker_api.execution_arn}/*"
}

output "api_url" {
  value = aws_apigatewayv2_api.job_tracker_api.api_endpoint
}