from imaplib import IMAP4
import traceback

from mail.listener import MailListener
from config import USERNAME, PASSWORD, IMAP_SERVER
from mail.handlers.handle_printing import handle_printing

if __name__ == '__main__':
    imap_server = 'outlook.office365.com'
    username = "mmenezes@viceri.com.br"
    password = "#450BRt300"

    while True:
        try:
            mail_listener = MailListener(
                username=USERNAME,
                password=PASSWORD,
                imap_server=IMAP_SERVER,
            )
            mail_listener.mail_handler.add_handler(handler=handle_printing)
            mail_listener.listen()
        except IMAP4.abort as e:
            print(e)
            print(traceback.format_exc())
            continue
