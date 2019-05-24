import boto3
import sys

#region and tier input from TC
region = str(sys.argv[1])
region = region.split(',')
tier = str(sys.argv[2])
tier = tier.split(',')

prod = []
nonprod = []
#rollback = []
all_tiers = []
status=0

#complete tag names
prod = map(( lambda x: x+ '_prod_asg' ), tier)
nonprod = map(( lambda x: x+ '_preprod_asg' ), tier)

#removed rollbacktag check
#rollback = map(( lambda x: x+ '_rollback_asg' ), tier)

#removed rollbacktag check
#all_tiers = prod + nonprod + rollback
all_tiers = prod + nonprod
all_tiers.sort()

def check_regions(region):
    for i in region:
        asg = boto3.client('autoscaling', region_name=i)

        #Create dictionary for tag = asg1,2,etc
        tagdict = dict((key, []) for key in all_tiers)
        #ask AWS for data
        response = asg.describe_tags(
            Filters=[
                {
                    'Name': 'key',
                    'Values':
                        all_tiers,
                },
            ],
        )

        #populate dictionary values
        def pop_tag_values():
            for tag in response['Tags']:
                tagdict [(tag['Key'])].append(tag['ResourceId'])

        #check ASG for issues with tags
        def check_asg_counts():
            for key, value in sorted(tagdict.items()):
                if len(value) != 1:
                    a = (i,"\t-", key, "=", value, "***ERROR - only one tag per ASG")
                    print ' '.join(map(str, a))
                    global status
                    status = 1

        pop_tag_values()
        check_asg_counts()
check_regions(region)

exit(status)
