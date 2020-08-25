import sqlite3

try:
    contacts=sqlite3.connect("data/contacts.db")
    contacts=contacts.execute('''CREATE TABLE CONTACTS(NAME TEXT,PASSWORD TEXT)''')
    contacts.commit()
    contacts.close()
except:
    pass

try:
    chats=sqlite3.connect("data/chatsroom.db")
    chats=chats.execute('''CREATE TABLE CHAT(CHAT TEXT,PERSON1 TEXT,PERSON2 TEXT) ''')
    chats.commit()
    chats.close()
except:
    pass

try:
    messages=sqlite3.connect("data/message.db")
    messages.execute('''CREATE TABLE MSG(CHAT TEXT,SENDER TEXT,RECIVER TEXT,MSG TEXT,TYPE TEXT,ID INT) ''')
    messages.commit()
    messages.close()
except:
    pass


def addcontacts(user,password):
    #add new contact

    contacts=sqlite3.connect("data/contacts.db")
    contacts.execute('''INSERT INTO CONTACTS(NAME , PASSWORD) VALUES(?,?)''',(user,password))
    contacts.commit()
    contacts.close()


def listcontacts():
    #return the list of contacts
    contacts=sqlite3.connect("data/contacts.db")
    contact=contacts.execute('''SELECT NAME FROM CONTACTS''')
    listcontact=[x[0] for x in contact.fetchall()]
    contacts.commit()
    contacts.close()
    return listcontact

def passwords(name):
    contacts=sqlite3.connect("data/contacts.db")
    password=contacts.execute('''SELECT PASSWORD FROM CONTACTS WHERE NAME=?''',(name,))
    password=password.fetchall()[0]
    contacts.commit()
    contacts.close()
    return password

def addchat(chat,person1,person2):
    #add new chat
    contacts=sqlite3.connect("data/chatsroom.db")
    contacts.execute('''INSERT INTO CHAT(CHAT,PERSON1,PERSON2) VALUES(?,?,?)''',(chat,person1,person2))
    contacts.commit()
    contacts.close()


def listchats(person):
    if person==None :
        #return the list of all chats
        chats=sqlite3.connect("data/chatsroom.db")
        chat=chats.execute('''SELECT CHAT FROM CONTACTS''')
        listchat=[x[0] for x in chat.fetchall()]
        chats.commit()
        chats.close()
        return listchat

    else:
        #return the all chat of that person
        chats=sqlite3.connect("data/chatsroom.db")
        chat=chats.execute('''SELECT * FROM CHAT WHERE PERSON1=? or person2=?''',(person,person))
        listchat=chat.fetchall()
        chats.commit()
        chats.close()
        return listchat


def addmsg(chat,sender,reciver,msg,type):
    #add new message
    messages=sqlite3.connect("data/message.db")
    messages.execute('''INSERT INTO CHAT(CHAT,SENDER,RECIVER,MSG,TYPE) VALUES(?,?,?,?,?)''',(chat,sender,reciver,msg,type))
    messages.commit()
    messages.close()


def listmsg(chat):
    #return the all msg of the chat
    messages=sqlite3.connect("data/message.db")
    message=messages.execute('''SELECT (SENDER,RECIVER,MSG,TYPE) FROM MSG WHERE CHAT=?''',(chat,))
    listmsgs=message.fetchall()
    messages.commit()
    messages.close()
    return listmsgs
