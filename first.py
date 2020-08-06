from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
# import smtplib
from flask_mail import Mail


with open("config.json", "r") as c:
    params = json.load(c)["params"]


app = Flask(__name__)
app.config.update(
    Mail_SERVER='sntp.gmail.com',
    Mail_PORT='465',
    Mail_USE_SSL=True,
    Mail_USERNAME=params["username"],
    Mail_PASSWORD=params["password"]

)
if params['local_server']:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

db = SQLAlchemy(app)
mail = Mail(app)


# def sendmail(to, content):
#     server = smtplib.SMTP('smntp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.login("rishikumargautam5002@gmail.com", "5+0+0+2=5002")
#     server.sendmail("rishikumargautam5002@gmail.com", to, content)
#     server.close()


class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Post(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sr = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(800), nullable=False)
    subheading = db.Column(db.String(800), nullable=False)
    slug = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(1200), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    posts = Post.query.filter_by().all()
    print(posts)
    return render_template('index.html', params=params, posts=posts)


@app.route("/home")
def home2():
    posts = Post.query.filter_by().all()

    return render_template('index.html', params=params, posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    print(post)
    return render_template('post.html', post=post, params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        # mail.send_message(
        #     "New Message From" + name,
        #     sender=email,
        #     recipients=[params["username"]],
        #     body=message + "\n" + phone
        #
        # )
        f = open("C:\\Users\\Rishi\\Desktop\\database for web.TXT", 'r+')
        content = f.read()
        f.write(f"--------------------------------\n{name} sent a message to you.\n{email}\n{phone}\n\n{message}\n--------------------------------")

    return render_template('contact.html', params=params)


app.run(debug=True)
