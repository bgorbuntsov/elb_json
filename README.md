# Fetch AWS ELB params into JSON file

For that we need a script that gets the following properties from AWS:
for each load balancer -
- name
- tags
- internal ip addresses
- external ip addresses

After getting these properties, for each load balancer, a json file is generated (file sample attached in comments)
The ID and BIOS-UUID fields are to be filled with the combination of load balancer name and AWS account id (example "test-load-balancer-123456789")

## Prerequisites
1. AWS credentials file

## Usage

*./scan.py vpc-id*

Running without parameters shows all VPCs.



