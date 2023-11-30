from flask import Flask,request, Response, render_template 
import uuid 
import time 
from flask_cors import CORS 
import json 
 
app = Flask(__name__,static_url_path='/static') 
 
CORS(app) 
 
app = Flask(__name__) 
 
users = {} 
msg = [] 
name = '' 
text = '' 
 
 
@app.route('/') 
def main(): 
    return render_template ('index.html') 
 
 
@app.route('/auth') 
def auth(): 
    name = request.args.get('name') 
    if name not in users: 
        token = str(uuid.uuid4()) 
        users[name] = token 
        return Response(token, status = 200, mimetype = "text/plain") 
    elif name == None: 
        return Response('you didn't provide a name',status = 400, mimetype = "text/plain") 
    else: 
        return Response('there is already such a user',status = 403, mimetype = "text/plain") 
 
 
@app.route('/users') 
def usersss(): 
    return (f'{users}') 
 
@app.route('/send') 
def send(): 
    text = request.args.get('text') 
    token = request.args.get('token') 
    if text == None: 
        return Response('the text is not specified',status = 400) 
    if token == None: 
        return Response('the text is not specified',status = 400) 
    name = None 
    for key,value in users.items(): 
        if value == token: 
            name = key 
    if name == None: 
        return Response('the name is empty',status = 403, mimetype = "text/plain") 
     
    timestamp = time.time() 
    msg.append({'name': name, 
                'text': text, 
                'time': timestamp}) 
    return Response('the message has been sent', status = 200, mimetype = "text/plain") 
     
     
     
@app.route("/logout") 
def logout(): 
    token = request.args.get('token') 
    if token == None: 
        return Response('the token is not specified',status = 400, mimetype = "text/plain") 
    for key,value in users.items(): 
        if value == token: 
            del users[key] 
            return Response('you have successfully logged out', status = 200, mimetype = "text/plain") 
    return Response('the token was not found',status = 403, mimetype = "text/plain") 
         
 
 
@app.route('/getall') 
def getall(): 
    token = request.args.get('token') 
    if token == None or token == "" or token not in users.values(): 
        return Response('The token was not found',status = 403) 
     
    return Response(json.dumps(msg), status = 200) 
 
 
if name == '__main__': 
    app.run(debug=True)