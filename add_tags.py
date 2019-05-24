#!/usr/bin/python

import boto3
import argparse
from inc.add_tag_to_instance import *
from inc.list_instances_by_tag_value import *

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--find_key", type=str,
                    help="Tag key we are looking for.")
parser.add_argument("-v", "--find_value", type=str,
                    help="Tag value we are looking for.")
parser.add_argument("-K", "--new_key",
                    help="Key to be added")
parser.add_argument("-V", "--new_value",
                    help="Value to be added")
args = parser.parse_args()

####Looking for this name in tags:
tagkey = args.find_key
tagvalue = args.find_value

ec2_match = list_instances_by_tag_value(tagkey, tagvalue)

newkey = args.new_key
newvalue = args.new_value

add_tag_to_instance(newkey, newvalue, ec2_match)
