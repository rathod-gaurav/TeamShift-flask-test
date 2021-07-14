from operator import index
from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect

from forms import LoginForm
from forms import ConfigForm
from forms import RegistrationForm

import datetime
import time
import pytz
tz = pytz.timezone('Asia/Kolkata')


import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd
import csv
import os

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


from flask_mail import Mail, Message

app = Flask(__name__)

#flask mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'noreply.teamshift@gmail.com'
app.config['MAIL_PASSWORD'] = 'ufmwhcggfkkqbbsu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['']
#app.config['']

mail = Mail(app)

#secret key for flask-forms
app.config['SECRET_KEY'] = 'b017acb0f2dea5916430f103839c0cd6'


#defining base route for reading/writing into files
#document_root = '/var/www/beta/'
document_root = ''


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@teamshift.org' and form.password.data == 'TeamSHIFT2021' and form.system_code.data == 'SHIFT001':
            if form.system_code.data == 'SHIFT001':
                tz = pytz.timezone('Asia/Kolkata')
                get_ts = datetime.datetime.now(tz).timestamp()
                readable_ts = time.ctime(get_ts)
                #ts = time.localtime()
                #readable_ts_2 = time.strftime("%Y-%m-%d %H:%M:%S", ts)

                #sending email that admin has logged in to the system
                msg = Message('SHIFT001 System Login', sender = 'noreply.teamshift@gmail.com', recipients = ['rathod.gauravvinod@gmail.com',
                                                                                                            '200010025@iitb.ac.in',
                                                                                                            'abhishekpm95202@gmail.com',
                                                                                                            'mlalwani0927@gmail.com',
                                                                                                            'nikhilyadav.07n@gmail.com'])
                msg.body = f"This email is generated at - \n {readable_ts}. \n Admin User has logged in to the system at {readable_ts}. \n Please donot reply to this email. \n Regards, \n Team SHIFT"
                mail.send(msg)

                flash(f"You have been logged in to the system at {readable_ts}", 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Login Unsuccessful! Please check your credentials', 'warning')
    return render_template('login.html', title='Login', form=form)

@app.route('/testing', methods=['GET'])
def testing():
    files = os.listdir('./')
    return str(files)

@app.route('/systemConfig', methods=['GET', 'POST']) #methods=['GET', 'POST']
def systemConfig():
    #show saved configurations
    config = pd.read_csv(document_root + 'config/config.csv', sep=',')

    form = ConfigForm()
    if form.validate_on_submit():
        config_df = pd.DataFrame(columns=['Growth Phase', 'Start Date', 'End Date',
                                        'Temp-LowerLimit', 'Temp-UpperLimit', 
                                        'pH-Lowerlimit', 'pH-UpperLimit', 
                                        'TDS-LowerLimit', 'TDS-UpperLimit',
                                        'Light(hrs/day)'])

        phase1 = [form.phase1_name.data, form.phase1_StartDate.data, form.phase1_EndDate.data,
                form.phase1_T_ll.data, form.phase1_T_ul.data,
                form.phase1_pH_ll.data, form.phase1_pH_ul.data,
                form.phase1_tds_ll.data, form.phase1_tds_ul.data,
                form.phase1_light.data]
        phase2 = [form.phase2_name.data, form.phase2_StartDate.data, form.phase2_EndDate.data,
                form.phase2_T_ll.data, form.phase2_T_ul.data,
                form.phase2_pH_ll.data, form.phase2_pH_ul.data,
                form.phase2_tds_ll.data, form.phase2_tds_ul.data,
                form.phase2_light.data]
        phase3 = [form.phase3_name.data, form.phase3_StartDate.data, form.phase3_EndDate.data,
                form.phase3_T_ll.data, form.phase3_T_ul.data,
                form.phase3_pH_ll.data, form.phase3_pH_ul.data,
                form.phase3_tds_ll.data, form.phase3_tds_ul.data,
                form.phase3_light.data]
        
        config_df = config_df.append({'Growth Phase': phase1[0], 'Start Date': phase1[1], 'End Date' : phase1[2],
                                    'Temp-LowerLimit' : phase1[3], 'Temp-UpperLimit' : phase1[4], 
                                    'pH-Lowerlimit' : phase1[5], 'pH-UpperLimit' : phase1[6], 
                                    'TDS-LowerLimit' : phase1[7], 'TDS-UpperLimit' : phase1[8],
                                    'Light(hrs/day)' : phase1[9]}, ignore_index=True)

        

        config_df = config_df.append({'Growth Phase': phase2[0], 'Start Date': phase2[1], 'End Date' : phase2[2],
                                    'Temp-LowerLimit' : phase2[3], 'Temp-UpperLimit' : phase2[4], 
                                    'pH-Lowerlimit' : phase2[5], 'pH-UpperLimit' : phase2[6], 
                                    'TDS-LowerLimit' : phase2[7], 'TDS-UpperLimit' : phase2[8],
                                    'Light(hrs/day)' : phase2[9]}, ignore_index=True)
        
        config_df = config_df.append({'Growth Phase': phase3[0], 'Start Date': phase3[1], 'End Date' : phase3[2],
                                    'Temp-LowerLimit' : phase3[3], 'Temp-UpperLimit' : phase3[4], 
                                    'pH-Lowerlimit' : phase3[5], 'pH-UpperLimit' : phase3[6], 
                                    'TDS-LowerLimit' : phase3[7], 'TDS-UpperLimit' : phase3[8],
                                    'Light(hrs/day)' : phase3[9]}, ignore_index=True)
        

        #save configuration settings into a .csv file
        config_df.to_csv(document_root + 'config/config.csv', index=False)

        get_ts = datetime.datetime.now(tz).timestamp()
        readable_ts = time.ctime(get_ts)
        flash(f"System Configured at {readable_ts}", "success")

        return redirect(url_for('homepage'))
    return render_template('config.html', title='Config.', form=form, 
                            tables = [config.to_html(classes = 'flags table')])

@app.route('/systemHomepage')
def homepage():
    config = pd.read_csv(document_root + 'config/config.csv', sep=',')

    #update homepage flags
    homepage_flags = pd.read_csv(document_root + 'files/homepage_flags.csv', sep=',')

    ts = time.localtime()
    readable_ts_2 = time.strftime("%Y-%m-%d %H:%M:%S", ts)

    for i in range(len(config.index)):
        if(readable_ts_2 == config.loc[i][1]):
            message = f"Current Growth Phase : {config.loc[i][0]}"
            if(homepage_flags.empty):
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][1], 'Message' : message})
            elif(message in homepage_flags['Message']):
                break
            else:
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][1], 'Message' : message})
        elif(readable_ts_2 == config.loc[i][2]):
            message = f"Change in Plant's Growth Phase : {config.loc[i][0]} => {config.loc[i+1][0]}"
            if(homepage_flags.empty):
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][2], 'Message' : message})
            if(message in homepage_flags['Message']):
                break
            else:
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][2], 'Message' : message})
    

    #update current status    
    current_status = pd.read_csv(document_root + 'files/current_status.csv', sep=',')

    for i in range(len(config.index)):
        if(readable_ts_2 == config.loc[i][1]):
            if(current_status.empty):
                current_status = current_status.append(config.loc[i])
                current_status.to_csv(document_root + 'files/current_status.csv', index=False)
            elif(config.loc[i][0] in current_status.iloc[0][0]):
                break
            else:
                current_status = current_status.append(config.loc[i])
                current_status.to_csv(document_root + 'files/current_status.csv', index=False)


    return render_template('homepage.html', title='Homepage',
                        #configuration table
                        tables = [config.to_html(classes = 'flags table')],
                        #homepage_flags_&_flags_table
                        tables2 = [homepage_flags.to_html(classes = 'flags table')])

@app.route('/systemTemperature')
def systemTemperature():

    # storage.child("data/sachin.txt").put("temp.txt")

    #start_time = time.time()

    #download file from firebase
    #storage.child("data/sachin.txt").download('data/sachin.txt', 'temp.txt')
    #time_Stage1 = time.time()

    #initializing an array to plot the graph
    data1 = np.loadtxt(document_root + 'test.txt', delimiter=',')
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
    file = open(document_root + 'temp_discrepancies.csv')
    reader = csv.reader(file)
    disc_num = len(list(reader))

    #checking for discrepancies
    for reading in range(np.size(data2)):
        if(data2[reading] >= var1):
            plt.plot(data3[reading], data2[reading], 'ro')
            #append message with timestamp that reading exceeded upper limit to another array
            get_ts = datetime.datetime.now(tz).timestamp()
            readable_ts = time.ctime(get_ts)
            message = "Temperature Exceeded above Upper Limit."
            df = pd.DataFrame({'timestamp' : readable_ts, 'message' : message}, index=[disc_num])
            disc_num += 1
            df.to_csv(document_root + 'temp_discrepancies.csv', mode='a', header=False)
            #code here
        elif(data2[reading] <= var2):
            plt.plot(data3[reading], data2[reading], 'b.')
            #append message with time stamp that reading went below lowerlimit to another array
            get_ts = datetime.datetime.now(tz).timestamp()
            readable_ts = time.ctime(get_ts)
            message = "System running low on Temperature."
            df = pd.DataFrame({'timestamp' : readable_ts, 'message' : message}, index=[disc_num])
            disc_num += 1
            df.to_csv(document_root + 'temp_discrepancies.csv', mode='a', header=False)
            #code here
    
    #push the discrepancy dataframe csv to firebase
    storage.child("temp/temp_discrepancies.csv").put(document_root + 'temp_discrepancies.csv')
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
    plt.savefig(document_root + 'temp_plot.png')

    #push the png image to firebase at a convenient location
    storage.child("images/temp.png").put(document_root + 'temp_plot.png')

    #finding other details
    average = np.mean(data1) #average of all readings
    size_x = np.size(data1) #total number of readings taken
    size_y = np.size(data2) #number of readings used for plotting
    current = data2[-1] #current reading

    #getting link of png image uploaded to firebase
    plot_link = storage.child("images/temp.png").get_url(None)

    #miscellaneous
    #end_time = time.time()
    #time_delay_end = end_time - start_time
    #time_delay_stage1 = end_time - time_Stage1

    #reading dataframe table for discrepancies
    discrepancies = pd.read_csv(document_root + 'temp_discrepancies.csv', sep=',', index_col='Index')

    return render_template('systemTemperature.html',
                            title='Temperature', temp=plot_link, t_avg=average,
                            t_count=size_x, t_count_y=size_y, t_curr=current,
                            #delay_end=time_delay_end, delay_stage1=time_delay_stage1,
                            #flags table
                            tables = [discrepancies.to_html(classes = 'flags table')],
                            )

@app.route('/systempH')
def systempH():
    return render_template('systempH.html', title='pH')

@app.route('/systemTDS')
def systemTDS():
    return render_template('systemtds.html', title='EC/TDS')

@app.route('/alertmessage')
def alert():
    #code for sending email messages
    tz = pytz.timezone('Asia/Kolkata')
    get_ts = datetime.datetime.now(tz).timestamp()
    readable_ts = time.ctime(get_ts)
    
    msg = Message('SHIFT001 System Update', sender = 'noreply.teamshift@gmail.com', recipients = ['rathod.gauravvinod@gmail.com',
                                                                            '200010001@iitb.ac.in',
                                                                            '200010025@iitb.ac.in'])
    msg.body = f"This email is generated at - \n {readable_ts}. \n This is a confirmation email. \n If you are receiving this email, then team SHIFT alert system is working fine! \n Please donot reply to this email. \n Regards, \n Team SHIFT"
    mail.send(msg)

@app.route('/sendData/<temp>/<ph>/<tds>')
def sendData(temp, ph, tds):
    with open('temperature.csv', 'a') as f:
        f.write(temp + ',' + ph + ',' + tds + "\n")

    return "Data Saved"

if __name__ == '__main__':
    app.run(debug=True)
