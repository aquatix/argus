import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='dev', 
    password='test')


stdin, stdout, stderr = ssh.exec_command("uptime")

print stdout.readlines()
