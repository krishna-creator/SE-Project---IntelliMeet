import unittest
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# email details
sender_email = "sid2lose@outlook.com"
receiver_email = "ch.premith.k@gmail.com"
subject = "Personlized Meeting Attentiveness summary"
body = "Body \n of the \nemail"
image_file = "client_graph.png"


# adding unit test to check if email address enterd is correct for USE CASE 1
def add_unit_test_1():
    # email details
    sender_email = "sid2lose@outlook.com"
    receiver_email = "ch.premith.k@gmail.com"
    subject = "Personlized Meeting Attentiveness summary"
    body = "Body \n of the \nemail"
    image_file = "client_graph.png"
    
        
    # msg = MIMEMultipart()
    # msg['From'] = sender_email
    # msg['To'] = receiver_email
    # msg['Subject'] = subject
    
    
    # msg.attach(MIMEText(body, 'plain'))
    
    # # add image to the message
    # with open(image_file, 'rb') as fp:
    #     img = MIMEImage(fp.read())
    # img.add_header('Content-Disposition', 'attachment', filename='image.png')
    # msg.attach(img)

    # connect to SMTP server and send email
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    smtp_username = "sid2lose@outlook.com"
    smtp_password = ""
    
    return smtp_server

    # with smtplib.SMTP(smtp_server, smtp_port) as server:
    #     server.starttls()
    #     server.login(smtp_username, smtp_password)
    #     server.sendmail(sender_email, receiver_email, msg.as_string())


# checking if the email authentication service is from OUTLOOK
class TestAdd(unittest.TestCase):
    def test_add(self):
        actual = add_unit_test_1()
        expected = "smtp-mail.outlook.com"
        self.assertEqual(actual, expected)