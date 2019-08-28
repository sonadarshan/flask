from flask import Flask, render_template, request,escape
from flask_mail import Mail
from flask_mail import Message
import pymysql
import json


class Post:
    def __init__(self, result):
        self.id = result[0]
        self.slug = result[1]
        self.date = result[2]
        self.heading = result[3]
        self.sub_heading = result[4]
        self.content = result[5]


with open('templates/config.json', 'r')as c:
    params = json.load(c)["params"]

if params["local_server"]:
    host = params["local_host"]
    user = params["local_user"]
    passwd = params["local_password"]
    database = params["local_database"]
else:
    host = params["prod_host"]
    user = params["prod_user"]
    passwd = params["prod_password"]
    database = params["prod_database"]


app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['mail_username'],
    MAIL_PASSWORD=params['mail_password']
)
mail = Mail(app)


@app.route('/')
def h():
    connection = pymysql.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM blogs')
    results = cursor.fetchall()
    posts = []
    for i in range(2):
        posts.append(Post(results[i]))
    return render_template('index.html', params=params, posts=posts)


@app.route('/index')
def home():
    connection = pymysql.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM blogs')
    results = cursor.fetchall()
    posts = []
    for i in range(5):
        posts.append(Post(results[i]))
    return render_template('index.html', params=params, posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        connection = pymysql.connect(host=host, user=user, passwd=passwd, database=database)
        cursor = connection.cursor()
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        insert = f"INSERT INTO users(Name,Phone,Email,Message) VALUES('{name}', '{phone}','{email}','{message}');"
        print(insert)
        cursor.execute(insert)
        connection.commit()
        msg = Message("New Message from Tradeport by ",
                      sender=params['mail_username'],
                      recipients=[params['mail_username']],
                      body=name+"\n"+message+'\n'+"Phone :"+phone+"\nEmail :"+email)
        mail.send(msg)
        cursor.close()
        connection.close()
    return render_template('contact.html', params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug='gann-strategy'):
    connection = pymysql.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = connection.cursor()
    insert = f'Select * from blogs where slug="{post_slug}"'
    cursor.execute(insert)
    result = cursor.fetchone()
    post = Post(result)
    return render_template('post.html', params=params, post=post)


@app.route("/dashboard")
def dashboard():
    return render_template('login.html')


app.run(debug=True)

