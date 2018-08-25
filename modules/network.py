import socket
import urllib.request


def get_local_hostname():
    return socket.getfqdn()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    result = s.getsockname()[0]
    s.close()
    return result


def get_public_ip():
    #external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    return external_ip
