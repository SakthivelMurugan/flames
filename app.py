from flask import Flask,render_template,request

app=Flask("__name__")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play")
def playGame():
    return render_template("play.html")

@app.route("/output",methods=["post","get"])
def outPut():
    str1=request.form.get("your")
    str2=request.form.get("crush")
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
    return render_template("output.html",data=dic)


if __name__=="__main__":
    app.run(debug=True)