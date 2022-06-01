from imapclient import IMAPClient
import email

from mail.mail_handler import MailHandler

# Função 'privada' para auxiliar a criação de um Mail 
def get_bodies(messages):
    unseen_messages = []
    for uid, content in messages.items():
        email_message = email.message_from_bytes(content[b'BODY[]'])
        unseen_messages.append((uid, email_message))
    return unseen_messages
    

class MailListener:
    def __init__(self, imap_server:str, username:str, password:str):
       self.server = IMAPClient(host=imap_server)
       self.server.login(username=username, password=password)
       self.mail_handler = MailHandler()

    @property
    def unseen(self):
        self.server.select_folder('INBOX')
        messages = self.server.search('UNSEEN')
        while True:
            unseen_messages = self.server.fetch(messages, ['BODY.PEEK[]'])
            try:
                return get_bodies(messages=unseen_messages)
            except KeyError:
                continue
            
    def listen(self):
        while True:
            for uid, mail in self.unseen:
                success = self.mail_handler.handle_mail(mail)
                if success: self.server.add_flags(uid, ['\\SEEN'])
            self.server.idle()
            self.server.idle_check(timeout=500)
            self.server.idle_done()

