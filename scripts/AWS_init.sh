#!/usr/bin/env bash

#Terraform initialization :
terraform init

#Creating a new EC2 instance, with inputs for ami_id,name :
terraform apply -auto-approve

#Creating a new S3 bucket, with inputs for bucket name :
python create_bucket.py

#Display instances IP and Public DNS Name :
aws ec2 describe-network-interfaces --query NetworkInterfaces[*].[Attachment.[InstanceId],Association.[PublicDnsName]] --output=json
aws ec2 describe-network-interfaces --query NetworkInterfaces[*].[Attachment.[InstanceId],Association.[PublicIp]] --output=json


