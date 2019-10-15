import boto3
import argparse
from inc.get_asg_ips import *
from inc.terminate_ASG import *
from inc.stop_workers_hup_processes import *

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--asg_tag_key",
                    help="Name of tag key on ASG to iterate")
parser.add_argument("-v", "--asg_tag_value",
                    help="Name of tag value on ASG to iterate")
parser.add_argument("-r", "--region",
                    help="region")

args = parser.parse_args()

region = args.region
asg_tag_key = [ args.asg_tag_key ]
asg_tag_value = [ args.asg_tag_value ]
protected_tags = [ "provisionworker_prod_asg", "provisionworker_preprod_asg", "provisionworker_rollback_asg" ]
ASGS = [ ]
private_ip = [ ] # List to hold the Private IP Address
protected_ASGS = [ ]
ASGS_targeted = [ ]
#should contain ASG name and list of IPs
final_dict = {}

def remove_protected_asgs(ASGS, protected_ASGS, ASGS_targeted):
    #clean up list for duplicates
    protected_ASGS = list(set(protected_ASGS))
    print("Protected ASGS are: {}" .format(protected_ASGS))
    #remove protected from ASGS list
    #ASGS_targeted = [x for x in ASGS if x not in protected_ASGS]
    for x in ASGS:
        if x not in protected_ASGS:
            ASGS_targeted.append(x)
    if len(ASGS_targeted) == 0:
        print("There is nothing to do. Only prod/preprod/rollback left")
        exit(0)
    print("ASG's to be targeted {}" .format(ASGS_targeted))
    return ASGS_targeted


def protected_asgs(protected_ASGS, region):
    asg = boto3.client('autoscaling', region_name=region)
    response = asg.describe_tags(
        Filters=[
        {
            'Name': 'key',
	        'Values':
            protected_tags
        },
        ],
        )
    for i in (response['Tags']):
        protected_ASGS.append(i['ResourceId'])
    return protected_ASGS


def create_list_ASGS(asg_tag_key, asg_tag_value, region, ASGS):
    #for i in region:
    asg = boto3.client('autoscaling', region_name=region)
    response = asg.describe_tags(
        Filters=[
        {
            'Name': 'key',
	        'Values':
            asg_tag_key
        },
        {
            'Name': 'value',
            'Values':
            asg_tag_value
        },
        ],
        )
    for i in response['Tags']:
        ASGS.append(i['ResourceId'])
    return ASGS

def get_ips(final_dict):

    for j in ASGS_targeted:
        ips = get_asg_ips(region, j)
        if type(ips) == type(None):
            print("Skipping")
        else:
            final_dict[j] = ips

create_list_ASGS(asg_tag_key, asg_tag_value, region, ASGS)
protected_asgs(protected_ASGS, region)
remove_protected_asgs(ASGS, protected_ASGS, ASGS_targeted)
get_ips(final_dict)

print("We'll be working on the following ASG: {}" .format(final_dict))
#stop workers from taking new jobs. Safely shut down processes
for k, v in sorted(final_dict.items()):
    stop_pw(v)
