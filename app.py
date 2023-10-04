
from flask import Flask, jsonify, redirect, render_template, request, url_for, json, session, flash
import collections
from pandas.core.arrays import string_
import pyrebase
import os
import datetime
from datetime import date
import smtplib
from email.message import EmailMessage
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import pandas as pd
from pandas import read_csv
import statsmodels.api as sm
from email import message
import nltk
import tflearn
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer
import random,json
#import chatty
from tensorflow.python.framework import ops

#-------------------Firebase Confugaration---------------------------
config = {
    "apiKey": "AIzaSyCx3u4VEmF9YtlhBsJkIUI06sHovH8NBvw",
    "authDomain": "energy-16fd7.firebaseapp.com",
    "databaseURL": "https://energy-16fd7-default-rtdb.firebaseio.com",
    "projectId": "energy-16fd7",
    "storageBucket": "energy-16fd7.appspot.com",
    "messagingSenderId": "784880996011",
    "appId": "1:784880996011:web:fc51cf6f66b9a26c96f1ee",
    "measurementId": "G-69BV07JLYR"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


data1 = db.child("Logpower").get()

data = data1.val()

dict_user={}
email=""


currdate = datetime.datetime(2021, 6, 10)


#-------------------------Daily visualization-------------------------#
# currdate = date.today()
dictDaily={}

for key,value in data.items():
    compare = key.split(' ')
    compare= datetime.datetime.strptime(compare[0], '%Y-%m-%d')
    i = 1
    if(compare.day==currdate.day):
        for key1,value1 in value.items():
            dictDaily.update({i : value1})
            i=i+1

#Converting Dictionary in Jason format
Data0 = json.dumps(dictDaily,indent=2)

#------------------------Weekly Visualiszation------------------------#
#Getting current week dates    
# today = datetime.date.today()
today = datetime.date(2021, 6, 10)
weekday = today.isoweekday()
# The start of the week
start = today - datetime.timedelta(days=weekday)
# build a simple range
currweekdates = [start + datetime.timedelta(days=d) for d in range(7)]
currweekdates = [str(d) for d in currweekdates]
#print(currweekdates)

dictWeeky = {}
k = 1
for j in currweekdates:
    j=datetime.datetime.strptime(j, '%Y-%m-%d')
    for key,value in data.items():
        compare = key.split(' ')
        compare= datetime.datetime.strptime(compare[0], '%Y-%m-%d')
        if(compare.day==j.day and compare.month==j.month):
            energy=0
            for key1,value1 in value.items():
                energy=energy+float(value1['Energy(Wh)'])            
            dictWeeky.update({j.strftime('%Y-%m-%d') : energy})

for i in currweekdates:
    if i not in dictWeeky.keys():
        dictWeeky.update({i : 0})

Data1=json.dumps(dictWeeky,indent=2)
#----------------------Monthly Visualisation-----------------------
dictMonthly= {}
months=[1,2,3,4,5,6,7,8,9,10,11,12]

for i in months:
    sum=0
    for key,value in data.items():
        compare = key.split(' ')
        compare= datetime.datetime.strptime(compare[0], '%Y-%m-%d')
        if(compare.month==i):
            for key1,value1 in value.items():
                sum=sum+float(value1['Energy(Wh)'])
                dictMonthly.update({compare.month : sum})

for i in months:
    if i not in dictMonthly.keys():
        dictMonthly.update({i : 0})

dictMonthly = collections.OrderedDict(sorted(dictMonthly.items()))
print(dictMonthly)
#------------------------Chatbot Confugaration------------------------
# stemmer=LancasterStemmer()
# with open("intents.json") as file:
# 	dataIntents = json.load(file)
# with open("data.pickle","rb") as f:
# 	words, labels, training, output = pickle.load(f)

# #Function to process input
# def bag_of_words(s, words):
# 	bag = [0 for _ in range(len(words))]
	
# 	s_words = nltk.word_tokenize(s)
# 	s_words = [stemmer.stem(word.lower()) for word in s_words]

# 	for se in s_words:
# 		for i,w in enumerate(words):
# 			if w == se:
# 				bag[i] = 1

# 	return np.array(bag)

# ops.reset_default_graph()

# net = tflearn.input_data(shape = [None, len(training[0])])
# net = tflearn.fully_connected(net,8)
# net = tflearn.fully_connected(net,8)
# net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
# net = tflearn.regression(net)

# #Loading existing model from disk
# model = tflearn.DNN(net)
# model.load("model.tflearn")
#----------------------------------------------------------------------

app = Flask(__name__)
model_forcast = pickle.load(open('predict.pkl', 'rb'))
app.secret_key = os.urandom(24)

stemmer=LancasterStemmer()
with open("intents.json") as file:
	dataIntents = json.load(file)
with open("data.pickle","rb") as f:
	words, labels, training, output = pickle.load(f)

#Function to process input
def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]
	
	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i,w in enumerate(words):
			if w == se:
				bag[i] = 1

	return np.array(bag)

ops.reset_default_graph()

net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
net = tflearn.regression(net)

#Loading existing model from disk
model = tflearn.DNN(net)
model.load("model.tflearn")

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        
        global email
        email=request.form['email']
        password=request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email,password)
            user_info=auth.sign_in_with_email_and_password(email,password)
            account_info=auth.get_account_info(user_info['idToken'])
            session['logged_in'] = True
            
            #if account_info['user'][0]['emailVerified']==False:
                 #verify_message='Please verify your email'
                 #return render_template('login.html',umessage=verify_message)
            
            return render_template("index.html",email=email,data=dictDaily, Data=dictWeeky, data1=dictMonthly)
            
        except:
            unsuccessful='Please check your credentials'
            return render_template("login.html",umessage=unsuccessful)

        
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return render_template("login.html")
    

    

@app.route('/register',methods=['GET','POST'])
def register():
    
    if request.method=='POST':
        pw0=request.form['pass']
        pw1=request.form['re_pass']
        if pw0==pw1:
            try:
                email=request.form['email']
                password=request.form['pass']

                userDict1={}
                mobileno=request.form['mobileno']
                userDict1.update({"Mobile_no":mobileno})

                mid=request.form['mid']
                userDict1.update({"Meter_Id":mid})

                First_name=request.form['First_name']
                userDict1.update({"First_name":First_name})

                Last_name=request.form['Last_name']
                userDict1.update({"Last_name":Last_name})

                Address=request.form['Address']
                userDict1.update({"Address":Address})

                City=request.form['City']
                userDict1.update({"City":City})

                State=request.form['State']
                userDict1.update({"State":State})

                Postal_Code=request.form['Postal_Code']
                userDict1.update({"Postal_Code":Postal_Code})

                if(len(email) == 0 and len(mobileno) == 0 and len(mid) == 0 and len(First_name) == 0 and len(Last_name) == 0 and len(Address) == 0 and len(City) == 0 and len(State) == 0 and len(pw0) == 0) :
                    existing_account='Please check your credentials'
                    return render_template("Register.html",exist_message=existing_account)

                new_user=auth.create_user_with_email_and_password(email,password)
                auth.get_account_info(new_user['idToken'])
                # auth.send_email_verification(new_user['idToken'])
                dict_user.update({email : userDict1})
                with open('users.txt', 'a+') as f:
                    for key, value in dict_user.items():
                        f.write('%s:%s\n' % (key, value)) 
                     
                return render_template("login.html") 
            except :
                existing_account='Email is alredy in use'
                return render_template("Register.html",exist_message=existing_account)
        else:
            password_incorrect='Password Not Matched, Please Enter Again!!'
            return render_template("Register.html",exist_message1=password_incorrect)

    return render_template("Register.html")


@app.route('/index')
def index():
    now = datetime.datetime.now()
    settime = now.replace(hour=22, minute=0, second=0, microsecond=0)

    EMAIL_ADDRESS = 'jproject20.21@gmail.com'
    EMAIL_PASSWORD = 'project2020'
    alertusage=str(dictDaily[22]["Energy(Wh)"])

    # if now == settime:
    msg = EmailMessage()
    msg['Subject'] = 'Usage for date '
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    msg.set_content('Usage for today is '+ alertusage +' Units')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)

    return render_template("index.html",data=dictDaily, Data=dictWeeky,email=email, data1=dictMonthly)

@app.route('/predict')
def predict():
    dforcast= {}
    #steps = int(request.form.values())
    pred_uc = model_forcast.get_forecast(10)
    output = pred_uc.predicted_mean
    #output = round(prediction[0], 2)
    #prediction_text='The price of this car should be $ {}'.format(output)
    output.index=output.index.astype(str)
    dforcast=output.to_dict()
    return render_template('predict.html',data=dforcast,email=email)

     
@app.route('/notifications')
def notification():
    return render_template("notifications.html")


@app.route('/user')
def user_info():
    userData0= {}
    with open ("users.txt",'r') as f:
        for line in f:
            userData = {}
            keyval= line.split(':',1)
            if email in str(keyval[0]):
                key_val_pairs = keyval[1].split(',')
                for kv_pair in key_val_pairs:
                    k_v = kv_pair.split(':')
                    key = str(k_v[0])
                    key=key.replace('"', '')
                    key=key.replace("{", "")
                    key=key.replace(' ','')
                    val = str(k_v[1])
                    val=val.replace('"', '')
                    val=val.replace("}", "")
                    val=val.replace('\n', '')   
                    userData.update({key : val})
                userData0.update({keyval[0]: userData})

    userJson = json.dumps(userData0,indent=2)
    return render_template("user.html",data=userData0,email=email)

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")


@app.route('/get')
def getBotResponse():
    message = request.args.get('msg')
    try:
        userReuestDate= datetime.datetime.strptime(message, '%Y-%m-%d') 
        for key,value in data.items():
            energy=0
            compare = key.split(' ')
            compare= datetime.datetime.strptime(compare[0], '%Y-%m-%d')
            if(compare.day==userReuestDate.day and compare.month==userReuestDate.month):
                for key1,value1 in value.items():
                    energy=energy+float(value1['Energy(Wh)'])            
                return "Energy consumption for given date is "+str(round(energy,2))
        if(energy==0):
            return "Energy consumption for given date is not available"

 
    except:
        if message:
            message=message.lower()
            results = model.predict([bag_of_words(message,words)])[0]
            result_index = np.argmax(results)
            tag = labels[result_index]
            if results[result_index]>0.5:
                for tg in dataIntents['intents']:
                    if tg['tag']==tag:
                        responses=tg['responses']
                response = random.choice(responses)
            else:
                response = "I didn't quite get that!!!"
            return str(response)
        return "Missing Data"

if __name__ == "__main__":
    app.run(debug = True)
