from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import json

app=Flask("__name__")
app.secret_key="sakthi25"

@app.route("/",methods=["post","get"])
def logIn():
    if request.form.get("username")!=None:
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")

        conn=sql.connect("flames.db")
        cur=conn.cursor()

        cur.execute("select username from user")
        data=cur.fetchall()

        l=[]
        for i in data:
            l.append(i[0])

        for i in l:
            if i==username:
                flash("user already exist")
                return redirect(url_for("signUp"))
        flash("user registered successfully")
        cur.execute("insert into user (username,email,password) values (?,?,?)",(username,email,password))
        conn.commit()

    return render_template("login.html")

@app.route("/signup")
def signUp():
    return render_template("signup.html")

@app.route("/adminlogin",methods=["post","get"])
def adminLogIn():
    return render_template("admin.html")

@app.route("/admin",methods=["post","get"])
def adminPanel():
    username=request.form.get("username")
    password=request.form.get("password")

    return render_template("adminpanel.html")

@app.route("/home",methods=["post","get"])
def home():
    username=request.form.get("username")
    password=request.form.get("password")

    conn=sql.connect("flames.db")
    cur=conn.cursor()
    cur.execute("select username,password from user")
    data=cur.fetchall()

    for i in data:
        if i[0]==username and i[1]==password:
            
            conn=sql.connect("flames.db")
            cur=conn.cursor()

            cur.execute("delete from loginuser")
            conn.commit()

            cur.execute("insert into loginuser (name) values (?)",(username,))
            conn.commit()

            return render_template("index.html",username=username)
    
    else:
        return redirect(url_for("logIn"))

@app.route("/play")
def playGame():
    return render_template("play.html")

@app.route("/playList")
def playList():
    conn=sql.connect("flames.db")
    cur=conn.cursor()
    cur.execute("select * from loginuser")
    data=cur.fetchall()
    data=data[-1][0]

    conn=sql.connect("flames.db")
    cur=conn.cursor()
    cur.execute("select * from playlist where username=?",(data,))
    data1=cur.fetchall()

    return render_template("playlist.html",data=data1)

@app.route("/output",methods=["post","get"])
def outPut():
    str1=request.form.get("your")
    str2=request.form.get("crush")
    yourname=str1
    crushname=str2

    l=[]
    for i in str1:
        if i!=" ":
            l.append(i)
    str1=l

    l=[]
    for i in str2:
        if i!=" ":
            l.append(i)
    str2=l
    i=0
    while i<len(str1):
        j=0
        while j<len(str2):
            if str1[i]==str2[j]:
                str1.pop(i)
                str2.pop(j)
                j=len(str2)-1
                i=i-1
            j+=1
        i+=1
    string=str1+str2
    l=len(string)
    array=["Friends","Lovers","Affectionate","Marriage","Enemies","Siblings"]
    pics={"Friends":"static/friends.jpg","Lovers":"static/love.jpg","Affectionate":"static/affection.jpg","Marriage":"static/marriage.jpg","Enemies":"static/enemy.jpg","Siblings":"static/siblings.jpg"}
    length=len(array)-1
    i=0 
    k=0
    while i<length:
        j=0
        while j<l:
            if k==len(array):
                k=0
            if j==l-1:
                array.pop(k)
                k-=1
            j+=1
            k+=1
        i+=1
    result=array[0]
    dic={"result":result,"pic":pics[result]}

    conn=sql.connect("flames.db")
    cur=conn.cursor()
    cur.execute("select * from loginuser")
    data=cur.fetchall()
    username=data[0][0]

    conn=sql.connect("flames.db")
    cur=conn.cursor()
    cur.execute("insert into playlist (username,yourname,crushname,flames) values (?,?,?,?)",(username,yourname,crushname,result))
    conn.commit()
    return render_template("output.html",data=dic)

@app.route("/feedBack")
def feedBack():
    return render_template("feedback.html")

@app.route("/thankpage")
def thank():
    return render_template("thank.html")

@app.route("/thank",methods=["post"])
def storeFB():
    output = request.get_json()
    
    conn=sql.connect("flames.db")
    cur=conn.cursor()
    cur.execute("select * from loginuser")
    username=cur.fetchall()

    username=username[0][0]
    feedback=output.get("name")
    emoji=output.get("path")

    conn=sql.connect("flames.db")
    cur=conn.cursor()
    cur.execute("insert into feedback (username,feedback,emoji) values (?,?,?)",(username,feedback,emoji))
    conn.commit()

    return render_template("thank.html")
     

if __name__=="__main__":
    app.run(debug=True)