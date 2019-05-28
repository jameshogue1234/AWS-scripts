import boto3
import sys


region_name = sys.argv[1]
tiers = sys.argv[2]
stage = sys.argv[3]
label = '_{}_asg'.format(stage)
tiers = tiers.split(',')
# make it a list
tier = map((lambda x: x+label), tiers)


ec2_client = boto3.client('ec2', region_name)
asg_client = boto3.client('autoscaling', region_name=region_name)


def get_asg_name():
    response = asg_client.describe_tags(
                Filters=[
                    {
                        'Name': 'key',
                        'Values':
                            tier,
                    },
                ],
            )
    for tag in response['Tags']:
        filtered_asgs = (tag['ResourceId'])
        return filtered_asgs
    # TODO add check to make sure you only find one 'filtered_asg'!!!


def get_asg_ips():
    asg = get_asg_name()
    asg_response = asg_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[asg]
        )

    # List to hold the instance-ids
    instance_ids = []

    for i in asg_response['AutoScalingGroups']:
        for k in i['Instances']:
            instance_ids.append(k['InstanceId'])

    ec2_response = ec2_client.describe_instances(
        InstanceIds=instance_ids
        )

    # List to hold the Private IP Address
    private_ip = []

    for instances in ec2_response['Reservations']:
        for ip in instances['Instances']:
            private_ip.append(ip['PrivateIpAddress'])

    # Print instance_ids
    print(",").join(private_ip)

get_asg_ips()

