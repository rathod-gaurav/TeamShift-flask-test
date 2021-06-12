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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd
import csv

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

    # storage.child("data/sachin.txt").put("temp.txt")

    start_time = time.time()

    #download file from firebase
    storage.child("data/sachin.txt").download('data/sachin.txt', 'temp.txt')
    time_Stage1 = time.time()

    #initializing an array to plot the graph
    data1 = np.loadtxt("temp.txt", dtype=int)
    #if number of entries in data1 < 100
    if(np.size(data1) < 100):
        data2 = data1
    else:
        data2 = data1[-100 : None]
    
    #initialize another array of size equal to data2
    data3 = range(np.size(data2))

    #plot dimensions
    plt.figure(figsize=(12,6))
    plt.clf()

    #defining lowerlimit and upperlimit
    var1 = 100 #upperlimit
    var2 = 40 #lowerlimit

    #find number of entries in the temp_discrepancies.csv file
    file = open('temp_discrepancies.csv')
    reader = csv.reader(file)
    disc_num = len(list(reader))

    #checking for discrepancies
    for reading in range(np.size(data2)):
        if(data2[reading] >= var1):
            plt.plot(data3[reading], data2[reading], 'ro')
            #append message with timestamp that reading exceeded upper limit to another array
            get_ts = datetime.datetime.now().timestamp()
            readable_ts = time.ctime(get_ts)
            message = "Temperature Exceeded above Upper Limit."
            df = pd.DataFrame({'timestamp' : readable_ts, 'message' : message}, index=[disc_num])
            disc_num += 1
            df.to_csv('temp_discrepancies.csv', mode='a', header=False)
            #code here
        elif(data2[reading] <= var2):
            plt.plot(data3[reading], data2[reading], 'b.')
            #append message with time stamp that reading went below lowerlimit to another array
            get_ts = datetime.datetime.now().timestamp()
            readable_ts = time.ctime(get_ts)
            message = "System running low on Temperature."
            df = pd.DataFrame({'timestamp' : readable_ts, 'message' : message}, index=[disc_num])
            disc_num += 1
            df.to_csv('temp_discrepancies.csv', mode='a', header=False)
            #code here
    
    #push the discrepancy dataframe csv to firebase
    storage.child("temp/temp_discrepancies.csv").put("temp_discrepancies.csv")
    #get link to this file from firebase
    temp_disc_csv_link = storage.child("temp/temp_discrepancies.csv").get_url(None)

    #final plot
    plt.xlim(min(data3) - 2, max(data3) + 2)
    plt.ylim(min(data2) - 10, max(data2) + 10)
    plt.plot(data3, data2)
    #horizontal lines representing lower and upper limits
    plt.axhline(y=var2, color='dodgerblue')
    plt.axhline(y=var1, color='tomato')
    #filling the plot
    plt.fill_between(data3, data2, -10, color = 'limegreen')
    #annotate current reading
    plt.annotate('Current Reading', xy = (data3[-1], data2[-1]))

    #saving the plot as a png file
    plt.savefig('temp_plot.png')

    #push the png image to firebase at a convenient location
    storage.child("images/temp.png").put("temp_plot.png")

    #finding other details
    average = np.mean(data1) #average of all readings
    size_x = np.size(data1) #total number of readings taken
    size_y = np.size(data2) #number of readings used for plotting
    current = data2[-1] #current reading

    #getting link of png image uploaded to firebase
    plot_link = storage.child("images/temp.png").get_url(None)

    #miscellaneous
    end_time = time.time()
    time_delay_end = end_time - start_time
    time_delay_stage1 = end_time - time_Stage1

    #reading dataframe table for discrepancies
    discrepancies = pd.read_csv(temp_disc_csv_link, sep=',', index_col='Index')

    return render_template('systemTemperature.html',
                            title='Temperature', temp=plot_link, t_avg=average,
                            t_count=size_x, t_count_y=size_y, t_curr=current,
                            delay_end=time_delay_end, delay_stage1=time_delay_stage1,
                            #flags table
                            tables = [discrepancies.to_html(classes = 'flags table')],
                            )

@app.route('/systempH')
def systempH():
    return render_template('systempH.html', title='pH')

@app.route('/systemTDS')
def systemTDS():
    return render_template('systemtds.html', title='EC/TDS')


if __name__ == '__main__':
    app.run(debug=True)