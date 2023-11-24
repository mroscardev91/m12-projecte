import smtplib, ssl
from email.message import EmailMessage
from email.utils import formataddr

class MailManager:

    def init_app(self, app):
        # agafo els paràmetres de configuració
        self.sender_name = app.config.get('MAIL_SENDER_NAME')
        self.sender_addr = app.config.get('MAIL_SENDER_ADDR')
        self.sender_password = app.config.get('MAIL_SENDER_PASSWORD')
        self.smtp_server = app.config.get('MAIL_SMTP_SERVER')
        self.smtp_port = app.config.get('MAIL_SMTP_PORT')
 
        # els missatges de contacte s'envien a aquesta adreça
        self.contact_addr = app.config.get('CONTACT_ADDR')

        # URL del servidor web
        self.external_url = app.config.get('EXTERNAL_URL')