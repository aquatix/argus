import http.client
import urllib


def send_message(settings, message, title="Argus"):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": settings.PUSHOVER_APP_TOKEN,
                     "user": settings.PUSHOVER_USER_KEY,
                     "message": message,
                     "title": title,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()
