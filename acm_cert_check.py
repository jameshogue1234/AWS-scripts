#!/usr/bin/python
import boto3
import datetime
from datadog_checks.base import AgentCheck, ConfigurationError
from checks import AgentCheck

class acm_cert_check(AgentCheck):

    def check(self, instance):
        acm = boto3.client('acm')
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
                self.gauge('ol.system.cert.acm', diff, tags=["tier:acm", "component:"+CertName]) 

