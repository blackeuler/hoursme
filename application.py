from flask import Flask,render_template, request
from flask import request
from timeLogger import TimeLogger

app = Flask(__name__)

x=TimeLogger()

@app.route("/")
def displayJobs():
    jobs = x.showAllJobs()
    return f"The jobs are{jobs}"

@app.route("/home", methods=['GET',])
def home():
    
    return render_template("login.html")
@app.route("/login",methods=['POST'])
def login():
    x.user = request.form['user']
    x.passw = request.form['pass']
    results= None
    try:
        results = x.webRun()
    finally:
        x.close()
        x.__init__()
    return render_template("submitHours.html")