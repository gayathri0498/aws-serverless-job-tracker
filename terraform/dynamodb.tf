resource "aws_dynamodb_table" "job_applications" {
  name         = "job-applications"
  billing_mode = "PROVISIONED"

  read_capacity  = 1
  write_capacity = 1

  hash_key = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project     = "AWS Job Tracker"
    Environment = "dev"
  }
}