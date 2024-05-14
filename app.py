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
 

client=MongoClient(os.getenv('mongo_url'))
app.config["MONGO_URI"] = os.getenv('mongo_url')
db=client['Daviz']

@app.route('/')
def home():
        return render_template('home.html')
@app.route('/login')
def login():
        return "Hii"
  
if __name__ =='__main__':  
    app.run(debug = True)  