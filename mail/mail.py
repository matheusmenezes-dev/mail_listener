from email.message import EmailMessage
from email.header import decode_header
import os
import pickle
from datetime import datetime

def decode(text:str) -> str:
    result = ''
    decoded_text = decode_header(text)
    for byte_string, charset in decoded_text:
        # Caso o texto esteja em bytes, decodificar usando charset (caso exista) ou utf-8
        # no contrário, simplesmente passar a string como resultado (não precisa decodificar)
        if type(byte_string) == bytes:
            result += byte_string.decode(charset) if charset else byte_string.decode('utf-8')
        elif type(byte_string) == str:
            result += byte_string
    return result
    

class Mail:
    def __init__(self, mail) -> None:
        self.mail = mail

    @property
    def content(self) -> str:
        for part in self.mail.walk():
            if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                # O bloco abaixo verifica a existencia de charsets explicitados, e os utiliza
                # no decode caso existam. No contrário, o bloco segue com o decode utf-8.
                charsets = part.get_charsets()
                if charsets:
                    for charset in charsets:
                        if charset:
                            message = part.get_payload(decode=True)
                            return message.decode(charset)
                else:
                    message = part.get_payload(decode=True)
                    return message.decode()

    @property
    def sender_email(self) -> str:
        email = decode(self.mail.get('From'))
        if '<' in email:
            name, email = email.split(' <')
            return email[:-1]
        else : return email
    
    @property
    def sender_name(self) -> str:
        try:
            email = decode(self.mail.get('From'))
            name, email = email.split(' <')
            return name
        except:
            return None

    @property
    def subject(self) -> str:
        subject = self.mail.get('Subject')
        return decode(subject)

    @property
    def date(self) -> str:
        return decode(self.mail.get('Date'))

    @property
    def datetime(self) -> datetime:
        return datetime.strptime(self.date, '%a, %d %b %Y %X %z')
        
    @property
    def fdatetime(self) -> str:
        return self.datetime.strftime('%d%m%Y:%H%M%S')
    
    @property
    def path(self) -> str:
        return f"mail/received_mails/{self.fdatetime}"

    def serialize(self) -> None:
        os.makedirs(self.path, exist_ok=True)

        # O email serializado fica em uma pasta com o nome self.fdatetime
        # mas o arquivo também tem o nome de self.fdatetime, por isso esse join
        # é usado aqui.
        with open(os.path.join(self.path, self.fdatetime), 'wb') as f:
            pickle.dump(self, f)

    @property
    def attachments(self):
        return [attachment for attachment in self.iter_attachments()]

    def iter_attachments(self):
        for part in self.mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            if part.get_filename(): yield part 

    def download_attachments(self) -> str:
        downloaded_files_path = []
        for attachment in self.iter_attachments():
            fileName = attachment.get_filename()
            if fileName:
                filePath = os.path.join(os.path.join(self.path), os.path.basename(fileName))
                if not os.path.isfile(filePath):
                    with open(filePath, 'wb') as f:
                        f.write(attachment.get_payload(decode=True))
                    downloaded_files_path.append(filePath)
        return downloaded_files_path
        
    def _download_attachments(self) -> str:
        for part in self.mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            if fileName:
                filePath = os.path.join(os.path.join(self.path), os.path.basename(fileName))
                if not os.path.isfile(filePath):
                    with open(filePath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    return filePath
                        
    