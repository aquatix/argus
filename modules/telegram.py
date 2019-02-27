import http.client
import urllib


def send_message(settings, message, title="Argus"):
    message = "{}\n{}".format(title, message)
    conn = http.client.HTTPSConnection("api.telegram.org:443")
    conn.request("GET", "/bot{}/sendMessage".format(settings.TELEGRAM_BOTKEY),
                 urllib.parse.urlencode({
                     "chat_id": settings.TELEGRAM_CHATID,
                     "disable_web_page_preview": 1,
                     "text": message,
                 }))
    conn.getresponse()
