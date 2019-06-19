#!/usr/bin/python

import boto3
import argparse
from inc.add_tag_to_instance import *
from inc.list_private_ips_by_tag_value import *

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--find_key", type=str,
                    help="Tag key we are looking for.")
parser.add_argument("-v", "--find_value", type=str,
                    help="Tag value we are looking for.")
parser.add_argument("-K", "--new_key",
                    help="Key to be added")
parser.add_argument("-V", "--new_value",
                    help="Value to be added")
parser.add_argument("-r", "--region",
                    help="region")

args = parser.parse_args()

region = args.region

####Looking for this name in tags:
tagkey = args.find_key
tagvalue = args.find_value

ec2_match = list_private_ips_by_tag_value(region, tagkey, tagvalue)
