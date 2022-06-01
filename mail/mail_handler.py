from email.message import EmailMessage
from mail.mail import Mail
import traceback
from typing import Callable

class MailHandler:
    def __init__(self) -> None:
        self.functions = []

    def add_handler(self, handler:Callable):
        if not handler in self.functions:
            self.functions.append(handler)

    def handle_mail(self, mail:EmailMessage):
        for function in self.functions:
            function(Mail(mail))
        return True