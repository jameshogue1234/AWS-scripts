import boto3
import sys
key = str(sys.argv[1])
value = str(sys.argv[2])

'''
Example:
python asg_kv_tag_lookup.py <tag Name> <tag value>
python asg_kv_tag_lookup.py Production True
'''

client = boto3.client('autoscaling')
paginator = client.get_paginator('describe_auto_scaling_groups')
page_iterator = paginator.paginate(
    PaginationConfig={'PageSize': 100}
)

filtered_asgs = page_iterator.search(
    'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(
        key, value)
)

for asg in filtered_asgs:
    print asg['AutoScalingGroupName']
