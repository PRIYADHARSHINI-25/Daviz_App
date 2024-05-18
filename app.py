from flask import Flask, url_for, session, render_template, request,flash
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import MismatchingStateError
from pymongo import MongoClient
import os
from gridfs import GridFS
from charts import preprocess,chartvis
#import pandas as pd
#import os,gridfs

app = Flask(__name__)  
 
app.secret_key=os.getenv('flask_secret')
app.config["MONGO_URI"] = os.getenv('mongo_url')
client=MongoClient(os.getenv('mongo_url'))
db=client['Daviz']

try:
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth = OAuth(app)
    oauth.register(
        name='daviz',
        client_secret=os.getenv('clientsecret'),
        client_id=os.getenv('clientID'),
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
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
        redirect_uri=url_for('gsignin', _external=True)
        return oauth.daviz.authorize_redirect(redirect_uri=redirect_uri)


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
    
# @app.route("/chart",methods=['GET','POST'])
# def chart():
#     try:
#         filegrid=GridFS(db)
#         user = session.get('user')
#         email=user['email']
#         if request.method=='POST':
#             csvfile=request.files['upload_file']
#             # content.seek(0)
#             content=csvfile.read()
#             csv_id=filegrid.put(content,filename=csvfile.filename)
#             db.user.update_one({'email_id':email},{'$set':{'files':csv_id}})
#             grid_out = filegrid.get(csv_id)
#             data = grid_out.read()
#             option,df=preprocess(data)
#             df_dict = df.to_dict(orient='records')
#             db.user.update_one({'email_id':email},{'$set':{'dataframe':df_dict}})
#             types=['line','bar','pie']
#             return render_template("input.html",option=option,types=types)
#     except:
#          return "Not working"


# @app.route('/visualize',methods=['GET','POST'])
# def visualize():
#         return "Visualization working"


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("home.html")
  
if __name__ =='__main__':  
    app.run(debug = True)  