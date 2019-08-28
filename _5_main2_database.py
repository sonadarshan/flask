from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

@app.route('/')
def h():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="tradeport")
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
    return render_template('contact.html')


@app.route('/post')
def post():
    return render_template('post.html')


app.run(debug=True)

