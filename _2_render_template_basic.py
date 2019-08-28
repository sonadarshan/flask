from flask import Flask,render_template

app = Flask(__name__)


@app.route("/")
def function1():
    # Here I can include any type of scripting languages like HTML,CSS
    return render_template('index1.html')


@app.route("/about")
def function2():
    name = 'Sonadarshan N G'
    # before that we should have variable in HTML page we can send the values from python to HTML
    return  render_template('about1.html', html_name=name)


app.run()