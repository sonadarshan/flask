from flask import Flask, render_template, request
import pymysql
import json


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
@app.route('/')
def h():
    return render_template('index.html', params=params)


@app.route('/index')
def home():
    return render_template('index.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/contact',methods=['GET', 'POST'])
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
        cursor.close()
        connection.close()
    return render_template('contact.html', params=params)


@app.route('/post')
def post():
    return render_template('post.html')


app.run(debug=True)

