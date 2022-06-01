import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

from config import USERNAME, PASSWORD, SMTP_SERVER 

class MailDispatcher:
    def __init__(self, username:str, password:str, smtp_server:str) -> None:
        self.username = username
        self.password = password
        self.smtp_server = smtp_server
        self.pending_mails = []
    
    def create_mail(self, to:str, subject:str, body:str, attachments_path:list=[]):
    # Criando Header
        message = MIMEMultipart()
        message["From"] = self.username
        message["To"] = to
        message["Subject"] = subject
        message["Bcc"] = to  

    # Adicionando o body à mensagem
        message.attach(MIMEText(body, "plain"))

        # Adicionando attachments e codificando
        for filename in attachments_path: 
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)    
        # Adicionando header do attachment
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(filename)}",
            )
            message.attach(part)
        return message 

    def send_mail(self, message):
        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.ehlo()
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, message["To"], message.as_string())
        return message 

    def add_to_pending_mails(self, message):
        self.pending_mails.append(message)

    def send_pending_mails(self):
        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.ehlo()
            server.starttls()
            server.login(self.username, self.password)
            # Uma lista diferente para não iterar/alterar ao mesmo tempo
            pending_mails = [mail for mail in self.pending_mails]
            for message in pending_mails:
                try:
                    server.sendmail(self.username, message["To"], message.as_string())
                    self.pending_mails.remove(message)
                except:
                    breakpoint()
                    continue
            self.pending_mails = []

if __name__ == '__main__':
    mail_dispatcher = MailDispatcher(
        username=USERNAME,
        password=PASSWORD,
        smtp_server=SMTP_SERVER,
    )

    mail_dispatcher.add_to_pending_mails(mail_dispatcher.create_mail(
        to="mmenezes@viceri.com.br",
        subject="This is a test subject",
        body="this is a test body",
        attachments_path=['mail/Matheus_Menezes.pdf']
        ))

    mail_dispatcher.add_to_pending_mails(mail_dispatcher.create_mail(
        to="mmenezes@viceri.com.br",
        subject="This is a SECONDARY test subject",
        body="this is a SECONDARY test body",
        attachments_path=['mail/Matheus_Menezes.pdf']
        ))

    mail_dispatcher.send_pending_mails()