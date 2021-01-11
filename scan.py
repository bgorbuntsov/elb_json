#!/usr/bin/python3

import os
import sys
import boto3
import json
import copy

def main():

    AWS_REGION = "eu-central-1"
    try:    
        ec2 = boto3.resource('ec2', region_name=AWS_REGION)
    
        if len(sys.argv) < 2:
            print("No VPC ID provided. Showing all VPCs")
            client_ec2 = boto3.client('ec2')
            vpcs = client_ec2.describe_vpcs()["Vpcs"]
            for vpc in vpcs:
                print(vpc["VpcId"])
        else:
    
            client_ec2 = boto3.client('ec2')
            vpc_id = sys.argv[1]
            
            result_mask = {"assets":[{"id":"","bios-uuid":"","name":"","addresses":[],"labels":[]}]}
            
            nics = client_ec2.describe_network_interfaces()["NetworkInterfaces"]
            
            client_sts = boto3.client('sts')
            awsid = client_sts.get_caller_identity().get('Account')
    
            client_elbv2 = boto3.client('elbv2')
            
            response = client_elbv2.describe_load_balancers()
            balancers = list( filter( lambda x: x["VpcId"] == vpc_id, response["LoadBalancers"] ) )
            if len(balancers) > 0:
                for balancer in balancers:
                    addr_list = []
                    result = copy.deepcopy(result_mask)
                    arn = balancer["LoadBalancerArn"]
                    elb_id = arn.split("/")[-1]
                    lb_name = balancer["LoadBalancerName"]
                    tags = client_elbv2.describe_tags(ResourceArns=[arn])["TagDescriptions"][0]["Tags"]
                    for tag in tags:
                        tag["key"] = tag.pop("Key")
                        tag["value"] = tag.pop("Value")
                    azones = balancer["AvailabilityZones"]
                    for zone in azones:
                        if zone["LoadBalancerAddresses"]:
                            addr_list.append(zone["LoadBalancerAddresses"][0]["IpAddress"])
                            addr_list.append(zone["LoadBalancerAddresses"][0]["PrivateIPv4Address"])
                    for nic in nics:
                        if elb_id == nic["Description"].split("/")[-1]:
                            public_ip = nic["PrivateIpAddresses"][0]["Association"]["PublicIp"]
                            private_ip = nic["PrivateIpAddresses"][0]["PrivateIpAddress"]
                            addr_list.extend([public_ip, private_ip])
    
                    id = lb_name + "-" + awsid
                    result["assets"][0]["id"] = id
                    result["assets"][0]["bios-uuid"] = id
                    result["assets"][0]["name"] = lb_name
                    result["assets"][0]["addresses"] = addr_list
                    result["assets"][0]["labels"] = tags
                    filename = lb_name + ".json"
                    with open(filename, 'w') as outfile:
                        json.dump(result, outfile, ensure_ascii=False, indent=2, default=str)
    
            else:
                print("No balancers here")
    except:
            print("Something went wrong")

if __name__ == "__main__":
    main()

