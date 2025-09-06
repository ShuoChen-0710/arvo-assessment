variable "aws_region" { type = string }
variable "instance_type" { type = string }
variable "open_ports" { type = list(number) }
variable "key_name" { type = string, default = null }
variable "user_data" { type = string }
