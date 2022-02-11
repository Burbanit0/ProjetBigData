#!/usr/bin/env bash

#Display instances IP and Public DNS Name :
aws ec2 describe-network-interfaces --query NetworkInterfaces[*].[Attachment.[InstanceId],Association.[PublicDnsName]] --output=json
aws ec2 describe-network-interfaces --query NetworkInterfaces[*].[Attachment.[InstanceId],Association.[PublicIp]] --output=json

#Asking to the user the public DNS name of the ec2 instance :
read -p "Instance public DNS :" dns

echo $dns

#Asking to the user the public ip of the ec2 instance :
read -p "Instance public ip :" ip

echo $ip

#Download data from hdfs
#hadoop fs -get /tmp/data/xdata.csv xdata.csv

#Encrypt file using a password
#./encrypt.sh -e -i data.csv -o data.enc -p toto

#Uploading files to the chosen ec2 instance via SSH
scp -i bigdata.pem xdata.csv ec2-user@${dns}:/home/ec2-user
scp -i bigdata.pem prediction.py ec2-user@${dns}:/home/ec2-user
scp -i bigdata.pem scaler.modele ec2-user@${dns}:/home/ec2-user
scp -i bigdata.pem modeleLineaire.modele ec2-user@${dns}:/home/ec2-user
scp -i bigdata.pem upload_file.py ec2-user@${dns}:/home/ec2-user

#Creating and uploading AWS credential in the ec2 instance :
ssh -i bigdata.pem ec2-user@${ip} 'aws configure'
scp -i bigdata.pem credentials ec2-user@${dns}:/home/ec2-user/.aws
scp -i bigdata.pem config ec2-user@${dns}:/home/ec2-user/.aws

#Installation of required python dependencies on the ec2 instance, starting machine learning script and uploading to chosen s3 bucket:
ssh -i bigdata.pem ec2-user@${ip} 'pip3 install boto3;pip3 install sklearn;pip3 install joblib;pip3 install pandas;python3 prediction.py;python3 upload_file.py'