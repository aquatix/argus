import paramiko
import subprocess

def remote_command(hostname, username, password, command, parameters):
    """
    Connect over ssh to hostname and execute the command on its shell
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('127.0.0.1', username='dev', password='password')
    ssh.connect(hostname, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.readlines()


def local_command(command, parameters=None):
    """
    Execute a shell command locally
    """
    #print subprocess.call(["ls", "-l"])
    if parameters != None:
        output = subprocess.Popen([command, parameters],
                                  stdout=subprocess.PIPE).communicate()[0]
    else:
        output = subprocess.Popen([command],
                                  stdout=subprocess.PIPE).communicate()[0]
    return output


def remote_argus_command(hostname, username, password, command, parameters):
    """
    Execute a command through the remote instance of Argus
    """
    pass


def get_volumes(raw_input):
    """
    Parse the sizes of storage volume 'volume'
    """
    volumes = raw_input.strip().split("\n")
    volumes.pop(0) # delete the header
    output = {}
    for volume in volumes:
        device, size, used, available, percent, mountpoint = \
            volume.split()
        output[mountpoint] = {'device': device, 'size': size, 'used': used, 'available': available, 'percent': percent, 'mountpoint': mountpoint}
    return output


def volume_available(all_volumes, mount_path):
    """
    Returns available storage of the volume mounted at mount_path in MB
    """
    return int(all_volumes[mount_path]['available']) / 1024


output = local_command('df')
all_volumes = get_volumes(output)
print all_volumes
print volume_available(all_volumes, '/home/mbscholt/data')

print local_command('ls', '-1')
print remote_command('127.0.0.1', 'test', 'password', 'ls', '-l')
