from django.core.mail import EmailMessage
import os
class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email='dkazi1996@gmail.com',
            to=[data['to_email']]
        )
        email.send()