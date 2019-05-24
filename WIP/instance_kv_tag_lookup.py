import boto3
import sys

key = str(sys.argv[1])
value = str(sys.argv[2])
'''
Example:
python instance_kv_tag_lookup.py <tag Name> <tag value>
python instance_kv_tag_lookup.py Production True
I also realize most of this was stolen...
'''
 
def list_instances_by_tag_value(tagkey, tagvalue):
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.
 
    ec2client = boto3.client('ec2')
 
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
            instancelist.append(instance["InstanceId"])
    return instancelist

print list_instances_by_tag_value(key, value)
