#!/usr/bin/python
import boto3
import datetime
from datadog_checks.base import AgentCheck, ConfigurationError
from checks import AgentCheck


class iam_cert_check(AgentCheck):

    def check(self, instance):
        iam = boto3.client('iam')
        date_format = "%m/%d/%Y"
        paginator = iam.get_paginator('list_server_certificates')
        for response in paginator.paginate():
            for i in response['ServerCertificateMetadataList']:
                CertName = i['ServerCertificateName']
                expiration = i['Expiration']
                bnew = (expiration.strftime("%Y-%m-%d"))
                today = datetime.date.today()
                m = int(expiration.strftime("%m"))
                d = int(expiration.strftime("%d"))
                Y = int(expiration.strftime("%Y"))
                future = datetime.date(Y, m, d)
                diff = future - today
                diff = str(diff)
                diff = diff.split(' ')[0]
                self.gauge('ol.system.cert.iam', diff, tags=["tier:iam", "component:"+CertName])

