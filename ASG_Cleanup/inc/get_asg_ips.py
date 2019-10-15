import boto3
from inc.terminate_ASG import *

def get_asg_ips(region, j):

    instance_ids = [ ] # List to hold the instance-ids
    private_ip = [ ] # Reset list to hold the Private IP Address
    asg_client = boto3.client('autoscaling', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)
    breaker = False

    asg = j
    #asg = "provisionworker_20190924075703_asg"
    print("Checking {} for ips: " .format(j))
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[j])

    for i in asg_response['AutoScalingGroups']:
     for k in i['Instances']:
         instance_ids.append(k['InstanceId'])
    if len(instance_ids) == 0:
        print("No instances running on ASG: {}" .format(j))
        terminate_ASG()
        return

    ec2_response = ec2_client.describe_instances(
         InstanceIds = instance_ids
         )
    #print(instance_ids) #This line will print the instance_ids

    for instances in ec2_response['Reservations']:
        if breaker:
            break
        for ip in instances['Instances']:
            try:
                private_ip.append(ip['PrivateIpAddress'])
            except:
                print("SecondTEST -- No instances running on ASG: {}" .format(j))
                terminate_ASG()
                breaker = True
                break
    print("{} has the following ips: {}" .format(j,private_ip))
    return private_ip
