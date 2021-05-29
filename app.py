from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect

from forms import LoginForm
from forms import RegistrationForm

import datetime
import time

import numpy as np
import matplotlib.pyplot as plt

import pyrebase

config = {
    "apiKey": "AIzaSyDYQDUyk3lN5Q9qoIc70iym3pQ-2_z-1Pc",
    "authDomain": "shift-ui-f9cec.firebaseapp.com",
    "databaseURL": "https://shift-ui-f9cec-default-rtdb.firebaseio.com",
    "projectId": "shift-ui-f9cec",
    "storageBucket": "shift-ui-f9cec.appspot.com",
    "messagingSenderId": "1062070212588",
    "appId": "1:1062070212588:web:57cafd0b3a9491156292c9",
    "measurementId": "G-HBDGWZTHJB"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


app = Flask(__name__)

app.config['SECRET_KEY'] = 'b017acb0f2dea5916430f103839c0cd6'

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@teamshift.org' and form.password.data == 'TeamSHIFT2021' and form.system_code.data == 'SHIFT001':
            if form.system_code.data == 'SHIFT001':
                get_ts = datetime.datetime.now().timestamp()
                readable_ts = time.ctime(get_ts)
                flash(f"You have been logged in to the system at {readable_ts}", 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Login Unsuccessful! Please check your credentials', 'warning')
    return render_template('login.html', title='Login', form=form)


@app.route('/systemHomepage')
def homepage():
    return render_template('homepage.html', title='Homepage')

@app.route('/systemTemperature')
def systemTemperature():
    storage.child("data/sachin.txt").download('data/sachin.txt', 'temp.txt')
    plt.clf()
    x = np.loadtxt("temp.txt", dtype=int)
    plt.plot(x)
    plt.savefig('temp_plot.png')
    storage.child("images/temp.png").put("temp_plot.png")
    average = np.mean(x)
    size = np.size(x)
    current = x[size-1]
    plot_link = storage.child("images/temp.png").get_url(None)
    return render_template('systemTemperature.html', title='Temperature', temp=plot_link, t_avg=average, t_count=size, t_curr=current)

@app.route('/systempH')
def systempH():
    return render_template('systempH.html', title='pH')

@app.route('/systemTDS')
def systemTDS():
    return render_template('systemtds.html', title='EC/TDS')


if __name__ == '__main__':
    app.run(debug=True)