data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = data.aws_vpc.default.id
}

# ELB
resource "aws_lb" "test" {
  name               = "test-lb-tf"
  internal           = false
  load_balancer_type = "network"
  subnets            = data.aws_subnet_ids.all.ids
  tags = local.tags
}

resource "aws_lb" "test2" {
  name               = "test-lb-tf2"
  internal           = false
  load_balancer_type = "network"
  subnets            = data.aws_subnet_ids.all.ids
  tags = local.tags
}

output "ARN" {
  value = aws_lb.test.arn
}
