output "ec2_public_ip" {
  value = aws_instance.streaming_server.public_ip
}