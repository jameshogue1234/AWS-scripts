import boto3
import argparse

def list_private_ips_by_tag_value(region, tagkey, tagvalue):
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.

    ec2client = boto3.client('ec2', region_name=region)

    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["PrivateIpAddress"])
    print "Found: %s" %(instancelist)
    return instancelist
