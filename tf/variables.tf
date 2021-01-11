variable "aws_access_key" {
  default = ""
}
variable "aws_secret_key" {
  default = ""
}
variable "my_ssh_pubkey" {
  default = ""
}

variable "aws_region" {
  default = "eu-central-1"

}
locals {
  tags = {
    author  = "Boris Gorbuntsov"
    mission  = "Catch All"
  }
}
