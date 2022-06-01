import unittest
from mail.mail import Mail
import pickle
from datetime import datetime

class TestMail(unittest.TestCase):
    def setUp(self):
        # Instancia de email.message.EmailMessage, serializada
        with open('tests/mock_models/EmailMessage.pckl', 'rb') as f:
            self.EmailMessage = pickle.load(f)
        # Instancia de mail.mail, serializada
        with open('tests/mock_models/25052022:132121', 'rb') as f:
            self.mailMessage = pickle.load(f)

    def test_get_sender_email(self):
        mail = Mail(self.EmailMessage)
        result = mail.sender_email
        target = 'matheusmenezes.dev@gmail.com'
        self.assertEqual(target, result)

    def test_get_subject(self):
        mail = Mail(self.EmailMessage)
        result = mail.subject
        target = 'This is a secondary test'
        self.assertEqual(target, result)

    def test_get_date(self):
        mail = Mail(self.EmailMessage)
        result = mail.date
        target = 'Sat, 28 May 2022 15:41:55 -0300'
        self.assertEqual(target, result)
    
    def test_get_datetime(self):
        mail = Mail(self.EmailMessage)
        result = mail.datetime
        self.assertTrue(type(result) == type(datetime.now()))
        
    def test_get_attachments(self):
        print(self.mailMessage.download_attachments())
        
