import paramiko
import subprocess
import sys, getopt

# The various types of commands argus supports:
CMD_HEALTH = 'health'
CMD_CHECKVOLUME = 'checkvolume'
CMD_REBOOTED = 'rebooted'


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


def main(argv):
    command = ''
    arguments = ''
    extra_arguments = ''
    remotehost = ''

    try:
        opts, args = getopt.getopt(argv,"hc:a:",["command=","arguments=","health","checkvolume=","rebooted"])
    except getopt.GetoptError:
        print 'node.py --<command> [<arguments>] [-r <remotehost>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'node.py --<command> [<arguments>] [-r <remotehost>]'
            print
            print 'Commands:'
            print '  health         do a generic health check on the configured items'
            print '  rebooted       the machine has rebooted, notify'
            print '  checkvolume    check the size of a mounted volume on the machine'
            print
            print 'Example:'
            print '  nody.py --checkvolume=<volume>    check the size of a mounted volume on the machine'
            sys.exit()
        elif opt in ("-r", "--remote"):
            remotehost = arg
        elif opt in ("-a", "--arguments"):
            extra_arguments = arg
        elif opt in ("--health"):
            command = CMD_HEALTH
        elif opt in ("-cv", "--checkvolume"):
            command = CMD_CHECKVOLUME
            arguments = arg
        elif opt in ("--rebooted"):
            command = CMD_REBOOTED
    print 'Command to execute is:', command
    print 'Provided arguments:', arguments
    print 'Extra arguments:', extra_arguments
    print 'Remote host:', remotehost

    if command == CMD_HEALTH:
        print 'Fetch config from db about what things to check health on'

    #print volume_available(all_volumes, '/home/mbscholt/data')
    if command == CMD_CHECKVOLUME:
        output = local_command('df')
        all_volumes = get_volumes(output)
        #print all_volumes
        print volume_available(all_volumes, arguments)

    if command == CMD_REBOOTED:
        print 'Machine rebooted, we should notify someone'

    #print local_command('ls', '-1')
    #print remote_command('127.0.0.1', 'test', 'password', 'ls', '-l')


if __name__ == "__main__":
    main(sys.argv[1:])
