from flask import Flask,render_template, request, session,url_for,redirect
from flask import request
from timeLogger import TimeLogger
from datetime import date
import datetime

app = Flask(__name__)
app.secret_key = 'hello'

seleniumSesssion={}


@app.route("/home", methods=['GET',])
def home():
    return render_template("login.html")
@app.route("/login",methods=['POST'])
def login():
    session["user"] = request.form['user']
    seleniumSesssion[session["user"]] = TimeLogger()
    print(len(seleniumSesssion))
    seleniumSesssion[session["user"]].user = session["user"]
    seleniumSesssion[session["user"]].passw = request.form['pass']

    seleniumSesssion[session["user"]].webLogin()
    jobs = seleniumSesssion[session["user"]].showJobs()
    return render_template("submitHours.html",jobs = jobs)
@app.route("/done", methods=['POST'])
def done():

    seleniumSesssion[session["user"]].selectJob(int(request.form['workplace'])+1)
    date = request.form["day"].split("-")
    dateP = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    seleniumSesssion[session["user"]].selectMonth(dateP.month)
    seleniumSesssion[session["user"]].goToDay(dateP)
    seleniumSesssion[session["user"]].enterHours(request.form['hours'])
    seleniumSesssion[session["user"]].close()
    session.pop('user', None)
    return redirect(url_for('home'))
    return render_template("login.html")
