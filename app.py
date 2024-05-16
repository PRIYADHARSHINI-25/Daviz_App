from flask import Flask, url_for, session, render_template, redirect, request,flash
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import MismatchingStateError
from pymongo import MongoClient
import os

# Create a MongoClient to the running mong
#from flask_pymongo import PyMongo,MongoClient
#from dotenv import load_dotenv
#import pandas as pd
#import os,gridfs
#from charts import preprocess,chartvis

app = Flask(__name__)  
 
app.secret_key=os.getenv('flask_secret')
#app.config["MONGO_URI"] = os.environ['mongo_url']
app.config["MONGO_URI"] = os.getenv('mongo_url')
client=MongoClient(os.getenv('mongo_url'))
#client=MongoClient(os.environ['mongo_url'])
db=client['Daviz']

try:
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth = OAuth(app)
    oauth.register(
        name='daviz',
        #client_id=os.environ['clientID'],
        #client_secret=os.environ['clientsecret'],
        client_secret=os.getenv('clientsecret'),
        client_id=os.getenv('clientID'),
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    print(client)
except:
     print("OAuth configuration error")

@app.route('/')
def home():
        return render_template('home.html')
@app.route('/login')
def login():
    try:
        if "user" in session:
                user = session.get('user')
                name=user['name']
                return render_template('fileupload.html',user=name)   
        else:
            return oauth.daviz.authorize_redirect(redirect_uri=url_for('gsignin', _external=True))
    except:
        return oauth.daviz.authorize_redirect(redirect_uri='/gsignin')
        # return oauth.daviz.authorize_redirect(redirect_uri=url_for('gsignin', _external=True))
@app.route('/dummy')
def dummy():
        return "Hello"


@app.route('/gsignin')
def gsignin():
    try:
        token = oauth.daviz.authorize_access_token()
        session['user'] = token['userinfo']
        user = session.get('user')
        name=user['name']
        email=user['email']
        profile=user['picture']
        # verify=user['email_verified']
        query={'email_id':email}
        doc ={'$set':{'email_id':email,'name':name,'profile':profile}}
        db.user.update_one(query,doc,upsert=True)
        return render_template('fileupload.html', user=name)
    except MismatchingStateError:
        flash('This action is not possible. Please try again.')
        return render_template("home.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("home.html")
  
if __name__ =='__main__':  
    app.run(debug = True)  