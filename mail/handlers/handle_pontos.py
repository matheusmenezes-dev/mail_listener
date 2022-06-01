from mail.mail import Mail
from processes.processar_pontos import processar_pontos
import traceback

def handle_pontos(mail:Mail):
    path = mail.download_attachments()
    return processar_pontos(path)
