from flask import Flask, url_for, redirect, request, render_template, json
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

app.config['PASSWORD'] = os.environ.get('PASSWORD')
#establishing the smtp server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 143
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vamsichowdary.dk@gmail.com'
app.config['MAIL_PASSWORD'] = app.config['PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = 'vamsichowdary.dk@gmail.com'
mail = Mail(app)

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

    #sending email to every paticipant
    for participant in participants:
        #formating the json object
        individual=[{'main' : participant}]
        others = [d for d in participants if d != participant]
        individual.append({'others' : others})

        #creating a json file
        with open('form_data.json', 'w') as f:
            json.dump(individual, f)
        msg = Message('Form Data', recipients=[participant['email']])
        msg.body = "Please see attached JSON file for form data."

        #attaching the json file
        with app.open_resource("form_data.json") as fp:
            msg.attach("form_data.json", "application/json", fp.read())
        mail.send(msg)

    participants = []
    return redirect(url_for('index'))



if __name__== "__main__":
    app.run(debug=True)  