from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import json 
import sqlite3
app=Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "dakey"
def database():
    conn=sqlite3.connect("../database/tasks.db")
    conn.row_factory=sqlite3.Row
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL)
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasktable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid INTEGER NOT NULL,
    title TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0)
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS notestable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL)
    """)
    conn.commit()
    return conn

@app.route('/')
    
@app.route('/home')
def home():
    if not session.get("uid"):
        return redirect('/login')
    conn= database()
    task_count = conn.execute("SELECT COUNT(id) FROM tasktable WHERE uid = ?", (session["uid"],)).fetchone()[0]
    note_count = conn.execute("SELECT COUNT(id) FROM notestable WHERE uid = ?", (session["uid"],)).fetchone()[0] 
    return render_template('home.html', tasks=task_count, notes=note_count)

@app.route('/calendar')
def about():
    return render_template('calendar.html') 

@app.route('/notes', methods=["GET", "POST"])
def note():
    if not session.get("uid"):
        return redirect('/login')
    conn = database()
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            conn.execute("INSERT INTO notestable(uid, title, content) VALUES (?, ?, ?)", (session["uid"], title, content))
            conn.commit()            
    ndata = conn.execute("SELECT * FROM notestable WHERE uid = ?", (session["uid"],)).fetchall()
    conn.close()
    return render_template('notes.html', notes=ndata)

@app.route('/notes/edit/<int:id>', methods=["GET", "POST"])
def edit_note(id):
    if not session.get("uid"):
        return redirect('/login')
    conn = database()
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            conn.execute("UPDATE notestable SET title=?, content=? WHERE id=?", (title, content, id))
            conn.commit()  
        conn.close()
        return redirect('/notes')
    note_to_edit = conn.execute("SELECT * FROM notestable WHERE id = ?", (id,)).fetchone()
    conn.close() 
    return render_template('edit_note.html', note=note_to_edit)

@app.route('/notes/delete/<int:id>', methods=["POST"])
def delete_note(id):
    conn = database()
    conn.execute("DELETE FROM notestable WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/notes')

@app.route('/tasks', methods=["GET", "POST"])
def tasks():
    if not session.get("uid"):
        return redirect('/login')
    conn = database()
    if request.method == "POST":
        task = request.form.get("task") 
        if task:
            ctask=task.strip()
        else:
            ctask=""
        if not ctask or len(ctask)>150:        
            return redirect('/tasks')

        conn.execute("INSERT INTO tasktable(uid, title, completed) VALUES (?, ?, ?)", (session["uid"], ctask, 0))
        conn.commit()

    tasks = conn.execute("SELECT * FROM tasktable WHERE uid = ?", (session["uid"],)).fetchall()
    conn.close()
    
    return render_template('tasks.html', tasks=tasks)
     
@app.route('/tasks/delete/<int:id>', methods=["POST"])
def delete_task(id):
    conn=database()
    conn.execute("DELETE FROM tasktable where id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/tasks')

@app.route('/tasks/toggle/<int:id>', methods=["POST"])
def check(id):
    conn=database()
    conn.execute("UPDATE tasktable SET completed = 1 - completed where id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/tasks')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        conn=database()
        try:
            hashed_password=generate_password_hash(password)
            conn.execute("INSERT into users (username,password) VALUES(?,?)",(username,hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "username already exists"
        finally:
            conn.close()        
        return redirect('/login')    
    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = database()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"],password):
            session["uid"] = user["id"]
            session["username"]=user["username"]
            return redirect('/tasks')
        return "invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/login')

@app.route('/api/student')
def student():
    return {
        "name": "Your Name",
    "college": "Madan Bhandari",
    "course": "BSc CSIT"
    }

if __name__ == '__main__':
    app.run(debug=True)
