import os


def needs_notifying(size_trigger, size_available):
    """Checks whether we need to send a notification

    Args:
    size_trigger: minimum amount of free space in GB
    size_available: currently available free space in bytes
    """
    return size_available <= (size_trigger * 1024*1024*1024)


def format_lowdisk_message(messages, hostname):
    return '[{}] Low disk space on the following volumes:\n{}'.format(hostname, '\n'.join(messages))


def check_diskspace(settings, hostname):
    try:
        filesystems = settings.FILESYSTEMS[hostname]
    except KeyError:
        return ('Error during diskspace check', '[spacealarm] No filesystem configuration found for {}'.format(hostname))

    messages = []

    for filesystem in filesystems:
        statvfs = os.statvfs(filesystem[0])

        #statvfs.f_frsize * statvfs.f_blocks     # Size of filesystem in bytes
        #statvfs.f_frsize * statvfs.f_bfree      # Actual number of free bytes
        #statvfs.f_frsize * statvfs.f_bavail     # Number of free bytes that ordinary users
                                                 # are allowed to use (excl. reserved space)

        if needs_notifying(filesystem[1], statvfs.f_frsize * statvfs.f_bavail):
            messages.append('{}: {:.1f}MB free'.format(filesystem[0], statvfs.f_frsize * statvfs.f_bavail / 1024/1024))

    if messages:
        return ('Diskspace warning', format_lowdisk_message(messages, hostname))
