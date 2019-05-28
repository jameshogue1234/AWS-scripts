import os
import subprocess
from subprocess import call
from datadog_checks.base import AgentCheck, ConfigurationError
from checks import AgentCheck
import os.path

class puppet_status(AgentCheck):

    def check_puppet_lastrun(self, last_run):
        #run the lastrun and get diff in seconds.
        bash_puppet = ['/usr/bin/sudo', '/usr/local/bin/datadog/check_puppet_lastrun.sh']
        last_run = subprocess.check_output(bash_puppet).decode("utf-8").strip()
        return(last_run)

    def check_puppet_branch(self, master):
        branch_file_check = "/etc/puppet/PUPPET_BRANCH"
        if os.path.isfile(branch_file_check):
            master=1
        else:
            master=0
        return(master)

    def check(self, instance):

        time_diff = self.check_puppet_lastrun(self)
        puppet_branch = self.check_puppet_branch(self)

        self.gauge('ol.system.puppet_lastrun', time_diff)
        self.gauge('ol.system.puppet_branch', puppet_branch)

