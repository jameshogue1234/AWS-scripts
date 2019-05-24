import boto3
import argparse

def add_tag_to_instance(newkey, newvalue, ec2_match):
    for i in ec2_match:
        print "Adding %s:%s to: %s" %(newkey, newvalue,i)
        ec2 = boto3.resource('ec2')
        ec2instance = ec2.Instance(i)
        tag_client = boto3.client('ec2')
        response = tag_client.create_tags(
            #DryRun=True|False,
            Resources=[
                i,
            ],
            Tags=[
                {
                    'Key': newkey,
                    'Value': newvalue
                },
            ]
        )
