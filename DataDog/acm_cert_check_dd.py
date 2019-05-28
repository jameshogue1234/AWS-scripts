#!/usr/bin/python
import boto3
import datetime
from datadog_checks.base import AgentCheck, ConfigurationError
from checks import AgentCheck

class acm_cert_check(AgentCheck):

    def check(self, instance):
        regions = ["us-west-1", "us-west-2", "us-east-1", "us-east-2", "eu-central-1", "eu-west-1"]
        for region in regions:
            acm = boto3.client('acm', region_name=region)
            paginator = acm.get_paginator('list_certificates')
            for response in paginator.paginate():
                for certificate in response['CertificateSummaryList']:
                    cert = certificate['CertificateArn']
                    details = acm.describe_certificate(
                        CertificateArn=cert
                    )
                    CertName=(details['Certificate']['DomainName'])
                    expiration=(details['Certificate']['NotAfter'])
                    bnew = (expiration.strftime("%Y-%m-%d"))
                    today = datetime.date.today()
                    m = int(expiration.strftime("%m"))
                    d = int(expiration.strftime("%d"))
                    Y = int(expiration.strftime("%Y"))
                    future = datetime.date(Y, m, d)
                    diff = future - today
                    diff = str(diff)
                    diff = diff.split(' ')[0]
                    self.gauge('ol.system.cert.acm', diff, tags=["tier:acm", "component:"+CertName, "region:"+region])

