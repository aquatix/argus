# -*- coding: utf-8 -*-
"""
    argus
    ~~~~~~

    A simple monitoring tool

    :copyright: (c) 2013-2023 by Michiel Scholten.
    :license: BSD, see LICENSE for more details.
"""

import click
import tabulate

import settings
from modules import diskspacealarm, network, pushover, smartctl, telegram

# get hostname for the current node
HOSTNAME = network.get_local_hostname()

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


## Main program
@click.group()
def cli():
    pass


@cli.command()
def check_diskspace():
    diskspace_info = diskspacealarm.check_diskspace(settings, HOSTNAME)
    if diskspace_info:
        pushover.send_message(settings, diskspace_info[1], title=diskspace_info[0])


@cli.command()
def rebooted():
    """Sends a message about the node having rebooted"""
    message = '[{}] Node has been rebooted. Local IP is {}, public IP is {}'.format(
        HOSTNAME,
        network.get_local_ip(),
        network.get_public_ip()
    )
    pushover.send_message(settings, message, title="Node has rebooted")


@cli.command()
@click.argument('message')
def send_message(message):
    """Sends a message"""
    title = '[{}] Message'.format(HOSTNAME)
    pushover.send_message(settings, message, title)


@cli.command()
def smartinfo():
    """Checks disks on health status"""
    devices = smartctl.get_devices()
    header, data = smartctl.get_information_on_drives(devices)
    for device in data:
        if device[header.index('Health')] != 'PASS':
            # There's something wrong with 'Health'
            message = smartctl.format_drive_info(header, device)
            # TODO: log this entry
            pushover.send_message(settings, message, title='[{}] Drive health warning'.format(HOSTNAME))


@cli.command()
def node_info():
    print('Node {}\nLocal IP is {}\nPublic IP is {}\n'.format(
        HOSTNAME,
        network.get_local_ip(),
        network.get_public_ip()
    ))
    diskspace_info  = diskspacealarm.check_diskspace(settings, HOSTNAME)
    if diskspace_info:
        print(diskspace_info[1])

    # S.M.A.R.T. drive info
    devices = smartctl.get_devices()
    header, data = smartctl.get_information_on_drives(devices)
    print(tabulate.tabulate(data, header, 'rst'))


if __name__ == '__main__':
    #init_db()
    cli()
