from flask import Flask,render_template, request
from flask import request
from timeLogger import TimeLogger
from datetime import date
import datetime

app = Flask(__name__)

x=TimeLogger()


@app.route("/home", methods=['GET',])
def home():
    return render_template("login.html")
@app.route("/login",methods=['POST'])
def login():
    x.user = request.form['user']
    x.passw = request.form['pass']
    x.webLogin()
    jobs = x.showJobs()
    return render_template("submitHours.html",jobs = jobs)
@app.route("/done", methods=['POST'])
def done():
    
    x.selectJob(int(request.form['workplace'])+1)
    date = request.form["day"].split("-")
    dateP = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    x.selectMonth(dateP.month)
    x.goToDay(dateP)
    x.enterHours(request.form['hours'])
    x.close()
    x.__init__()
    return render_template("login.html")