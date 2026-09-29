output "public_ip" {
  description = "Public IP address of the deployed AWS EC2 Portfolio server"
  value       = aws_instance.portfolio_server.public_ip
}

output "website_url" {
  description = "Live Website URL"
  value       = "http://${aws_instance.portfolio_server.public_ip}"
}
