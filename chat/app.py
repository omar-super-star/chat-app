import flask ,sqlite3
from flask import *
from data import *
from flask_socketio import SocketIO,emit,join_room,leave_room
import os
app=Flask(__name__)
app.config["SECRET_KEY"]="GHAGDTAGHJDGAJHGYGYGJHGYA12151884"
socket=SocketIO(app)
import json

@app.route("/")
def start():
    return redirect(url_for("sign"))
@app.route("/login",methods=["POST","GET"])
def login():
    #first page to enter the app
    names=listcontacts()
    if request.method=="POST":
        data=request.data
        data=json.loads(data)
        name=data["name"]
        password=data["password"]
        if name in names:
            return jsonify({"sucssess":"fail","error":"that name is not allowed"})
        else:
            addcontacts(name,password)
            return jsonify({"sucssess":"sucssess","error":"not error"})
    else:
        return render_template("login.html")


@app.route("/sign",methods=["POST","GET"])
def sign():
    names=listcontacts()
    if request.method=="POST":
        data=json.loads(request.data)
        name=data["name"]
        password=data["password"]
        if name in names:
            check_pass=passwords(name)
            print(check_pass)
            print(password)
            if not (password in check_pass):
                session["name"]=name
                return jsonify({"sucssess":"fail","error":"that password is incorrect"})
            else:
                return jsonify({"sucssess":"sucssess","error":"not error"})
        else:
            return jsonify({"sucssess":"fail","error":"that name is incorrect"})
    else:
        return render_template("sign.html")


@app.route("/contacts",methods=["POST","GET"])
def contacts():
    #here show contacts
    if request.method=="POST":
        names=listcontacts()
        name=request.data["name_serach"]
        if name in names:
            outname=name
        else:
            outname="name is not found "    
        return jsonify({"outlist":outname})
    else:
        person=session["name"]
        chat=listchats(person)
        return render_template("contact.html",chats=chat,name=person,space=" ")

@app.route("/chat/<chatroom>",methods=["POST","GET"])
def chat(chatroom):
    #page for chat room
    person1=session["name"]
    chat=chatroom
    chat.split()
    chat=chat.sort()
    if chat[0]==person1:
        person2=chat[1]
    else:
        person2=chat[0]    
    chat=chat[0]+chat[1]
    msg=listmsg(chat)
    return render_template("chat.html",msg=msg,length=len(msg),person1=person1,person2=person2)

    
@app.route("/media",methods=["POST","GET"])
def media():
    name=request.form.get("name")
    type=request.form.get("type")
    ord=request.form.get("ord")
    image=request.files.get("file")
    ext=image.filename.find(".")
    ext=image.filename[ext:]
    image.save(os.path.join(app.config["UPLOAD_FOLDER"],"profile_image/"+name+type+str(ord)+ext))
    file_name="profile_image/"+name+ext
    return jsonify({"msg":file_name})
@socket.on("join_room")
def roomjoin(data):
    sender= str(data['sender'])
    reciver=str(data["reciver"])
    room = str(data['room'])
    _type=str(data["type"])
    msg=str(data["msg"])
    if room in listchats(None):
        pass
    else:
        addchat(chat,sender,reciver)
    join_room(room)
    addmsg(room,sender,reciver,msg,type)
    socket.emit(room,data)
app.run()
