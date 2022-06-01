from mail.mail import Mail
import traceback

def handle_printing(mail:Mail):
    try:
        print('-' * 60)
        print("E-MAIL RECEBIDO!")
        print(f"DE: {mail.sender_name if mail.sender_name else ''} {mail.sender_email}")
        print(f"ASSUNTO: {mail.subject}")
        print(mail.content if len(mail.content) < 300 else f"{mail.content[:299]}...")
        print(f"ANEXOS: {len(mail.attachments)}" if mail.attachments else 'SEM ANEXOS')
        for attachment in mail.attachments:
            print(attachment.get_filename()) 
        print(mail.date)
        print('-' * 60)
        return True
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False
