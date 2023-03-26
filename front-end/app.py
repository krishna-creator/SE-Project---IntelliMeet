from flask import Flask, url_for, redirect, request, render_template, json
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import os

app = Flask(__name__)
load_dotenv()

app.config['PASSWORD'] = os.environ.get('PASSWORD')
password = app.config['PASSWORD']

participants=[]
@app.route('/', methods= ['GET', 'POST'])

def index():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        ipaddress = request.form['ipaddress']
        port = request.form['port']

        form_data = {
            'name': name,
            'email': email,
            'ipaddress': ipaddress,
            'port': port
        }
        participants.append(form_data)
        return redirect(url_for('index'))
    return render_template("index.html", participants=participants)

@app.route('/sendInvites', methods= ['GET', 'POST'])
def sendkInvites():
    global participants
    #establishing the smtp server
    sender_email = 'vamsichowdary.dk@gmail.com'
    sender_password = password
    message = MIMEMultipart()
    message['From'] = sender_email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = sender_password

    #sending email to every paticipant
    for participant in participants:
        #formating the json object
        individual=[{'main' : participant}]
        others = [d for d in participants if d != participant]
        individual.append({'others' : others})

        #creating a json file
        with open('form_data.json', 'w') as f:
            json.dump(individual, f)
        #creating email body
        message['Subject'] = 'Form Data'
        recipient_email = participant['email']
        message['To'] = recipient_email
        body = "Please see attached JSON file for form data."
        message.attach(MIMEText(body, 'plain'))
        with open('form_data.json', 'r') as f:
            attachment = MIMEApplication(f.read(), _subtype='json')
            attachment.add_header('Content-Disposition', 'attachment', filename='form_data.json')
            message.attach(attachment)
        #setting up the server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()

    participants = []
    return redirect(url_for('index'))



if __name__== "__main__":
    app.run(debug=True)  