from flask import Flask,render_template, request, session,url_for,redirect
from flask import request
from timeLogger import TimeLogger
from datetime import date
import datetime

app = Flask(__name__)
app.secret_key = 'hello'

seleniumSesssion={}


@app.route("/", methods=['GET',])
def home(errors=""):
    errors = request.args.get('errors',None)
    messages  = request.args.get('messages',None)

    # return render_template("login.html", errors = errors, messages = messages)
    return "hello world"
@app.route("/login",methods=['POST'])
def login():
    session["user"] = request.form['user']
    seleniumSesssion[session["user"]] = TimeLogger()
    seleniumSesssion[session["user"]].user = session["user"]
    seleniumSesssion[session["user"]].passw = request.form['pass']
    session["errors"] = None
    loginSuccess = seleniumSesssion[session["user"]].webLogin()
    if loginSuccess:    
        jobs = seleniumSesssion[session["user"]].showJobs()
        return render_template("submitHours.html",jobs = jobs)
    session["errors"] = ["Wrong Password Please try again"]
    return redirect(url_for('home',errors=session["errors"]))
@app.route("/done", methods=['POST'])
def done():
    try:
        seleniumSesssion[session["user"]].selectJob(int(request.form['workplace'])+1)
    except KeyError:
        print("The user is no longer present")
        return redirect(url_for('home'))
    date = request.form["day"].split("-")
    dateP = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    try:
        seleniumSesssion[session["user"]].selectMonth(dateP.month)
        seleniumSesssion[session["user"]].goToDay(dateP)
        seleniumSesssion[session["user"]].enterHours(request.form['hours'])
        seleniumSesssion[session["user"]].close()
        session.pop('user', None)
        return redirect(url_for('home',messages="hours logged succesfully"))
    except:
        print("something went wrong")
        return redirect(url_for('home',errors=['Did not find TimeSheet']))
