#coding:utf8     
from flask import Flask,render_template,request,redirect,session
from sqlalchemy import create_engine, MetaData  
import sqlite3
import datetime
app = Flask(__name__)
app.secret_key = '\xc0B$\xeb\xf2\xe7\xf4\xa0\xbc\xa1o7G\xef-\x8aN\xd8\x08\x017ZC\x18'

@app.route('/index/',methods=['GET','POST'])
def index():
    conn = sqlite3.connect('my.db')
    conn.text_factory=lambda x: unicode(x, "cp936", "ignore")
    cursor = conn.cursor()
    if request.method =='POST':
        text = request.form['text']
        text = text.encode('cp936')
        now = datetime.datetime.now()
        nowtime = now.strftime("%Y/%m/%d")
        addsql ="insert into liuyan(time,content) values(?,?)"
        cursor.execute(addsql,(nowtime,text))
        conn.commit()
    sql = "select title,id from blog "
    cursor.execute(sql)
    title = cursor.fetchall()

    sql = "select time,content from liuyan"
    cursor.execute(sql)
    liuyan = cursor.fetchall()
    
    cursor.close()
    conn.close()
        
    return render_template('index.html',title=title,liuyan=liuyan) 

@app.route('/admin/',methods=['GET','POST'])
def admin():
    if request.method == 'POST':	
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('my.db')
        cursor = conn.cursor()
        sql = "select * from admin"
        cursor.execute(sql)
        admin=cursor.fetchone() 
        if username ==admin[0] and password == admin[1]:
            session['login']=True
            return render_template('ggrxx.html')
        else:
            return render_template('login_fail.html')
    else:
        return render_template('login.html')

@app.route('/ggrxx/',methods=['GET','POST'])
def ggrxx():
    if not session.get('login'):
        return redirect('/admin/')
    if request.method == 'POST':	
        name = request.form['name']
        sex = request.form['sex']
        addr = request.form['addr']
        tel = request.form['tel']
        conn = sqlite3.connect('my.db')
        cursor = conn.cursor()
        if name !="":
            cursor.execute("update  person set name = %s where id =1"%name)
        if sex !="":
            cursor.execute("update  person set sex = %s where id =1"%sex)
        if addr !="":
            cursor.execute("update  person set addr =%s where id =1"%addr)
        if tel !="":
            cursor.execute("update  person set tel = %s where id =1"%tel)
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('ggrxx.html')
    else:
        return render_template('ggrxx.html')

@app.route('/grzx/')
def grzx():
    conn = sqlite3.connect('my.db')
    conn.text_factory=lambda x: unicode(x, "cp936", "ignore") 
    cursor = conn.cursor()
    sql = "select * from person"
    cursor.execute(sql)
    person=cursor.fetchone() 
    return render_template('grzx.html',name=person[0],sex=person[1],addr=person[2],tel=person[3])

@app.route('/blog/<id>',methods=['GET','POST'])
def blog(id):
    conn = sqlite3.connect('my.db')
    conn.text_factory=lambda x: unicode(x, "cp936", "ignore")
    cursor = conn.cursor()
    if request.method == 'POST':
        text = request.form['text']
        text = text.encode('cp936')
        now = datetime.datetime.now()
        nowtime = now.strftime("%Y/%m/%d")
        sql = 'insert into pinglun(time,content,blogid)values(?,?,?)'
        cursor.execute(sql,(nowtime,text,id))
        conn.commit()
    sql = "select title,content,tag from blog where id=%s"
    cursor.execute(sql%id)
    content = cursor.fetchone()
    tag = content[2]
    tag = tag.split('/')

    sql = "select time,content from pinglun where blogid=%s"
    cursor.execute(sql%id)
    pinglun = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('blog.html',content=content,pinglun=pinglun,tag=tag)

@app.route('/fbwz/',methods=['GET','POST'])
def fbwz():
    if not session.get('login'):
        return redirect('/admin/')
    if request.method == "POST":
        tagx = request.form['tag']
        tag = tagx.encode('cp936')
        titlex = request.form['title']
        title = titlex.encode('cp936')
        zhengwenx = request.form['zhengwen']
        zhengwen = zhengwenx.encode('cp936')
        conn = sqlite3.connect('my.db')
        conn.text_factory=lambda x: unicode(x, "cp936", "ignore")
        cursor = conn.cursor()
        sql="insert into blog(title,tag,content) values(?,?,?)"
        cursor.execute(sql,(title,tag,zhengwen))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('fbwz.html')
    else:
        return render_template('fbwz.html')
    
@app.route('/glwz/')
def glwz():
    if not session.get('login'):
        return redirect('/admin/')
    conn = sqlite3.connect('my.db')
    conn.text_factory=lambda x: unicode(x, "cp936", "ignore")
    cursor = conn.cursor()
    sql = "select title,id from blog "
    cursor.execute(sql)
    title = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('glwz.html',title=title)

@app.route('/dblog/<id>')
def dblog(id):
    if not session.get('login'):
        return redirect('/admin/')
    conn = sqlite3.connect('my.db')
    cursor = conn.cursor()
    sql = "delete from blog where id = ?"
    cursor.execute(sql,id)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/glwz/')

@app.route('/glpl/')
def glpl():
    if not session.get('login'):
        return redirect('/admin/')
    conn = sqlite3.connect('my.db')
    conn.text_factory=lambda x: unicode(x, "cp936", "ignore")
    cursor = conn.cursor()
    sql = "select time,content,id from liuyan "
    cursor.execute(sql)
    liuyan = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('glpl.html',liuyan=liuyan)

@app.route('/dliuyan/<id>')
def dliuyan(id):
    if not session.get('login'):
        return redirect('/admin/')
    conn = sqlite3.connect('my.db')
    cursor = conn.cursor()
    sql = "delete from liuyan where id = ?"
    cursor.execute(sql,id)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/glpl/')


app.route('/grzx/')
if __name__ == '__main__':
    app.debug = True
    app.run()
