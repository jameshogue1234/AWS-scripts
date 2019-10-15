import boto3
import paramiko


#1) "sudo su -c 'sudo sv stop workers'" --> stop it from collecting
#2) "sudo su -c 'sudo pkill -TERM -f provisioning_worker.rb'" --> safely kills workers
#3) "sudo su -c 'ps -ef | grep provision | grep -v grep'" --> final check





def stop_pw(ip):
    for i in ip:
        print(i)
        #host_ip = "10.8.1.130"
        host_ip = i
        user = "jhogue"
        ssh = paramiko.SSHClient()
        paramiko.util.log_to_file('/Users/jameshogue/WIP/ASG_Cleanup/paramiko.log')
        transport = ssh.get_transport()
        #transport.set_keepalive(30)

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='10.8.1.130', username='jhogue', key_filename='/Users/jameshogue/.ssh/id_rsa.pub')

        #logging.raiseExceptions=False
        stdin, stdout, stderr = ssh.exec_command('ls', timeout=10)
        ssh_stdout = stdout.readlines()
        print(ssh_stdout) #print the output of ls command
