from flask import Flask,render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index1.html')


@app.route("/hai")
def hai():
    return "Hello bro you are on the hai page"

# This can be used when we are making the changes and no need to run the app again again
# app.run(debug=True)

# To run the website normally
app.run()