from flask import Flask, render_template, request, redirect
import json 
import sqlite3
app=Flask(__name__, template_folder="../templates", static_folder="../static")

def database():
    conn=sqlite3.connect("../database/tasks.db")
    conn.row_factory=sqlite3.Row
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasktable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0)
    """)
    conn.commit()
    return conn

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/tasks',methods=["GET", "POST"])
def tasks():
    conn=database()
   
    if request.method=="POST":
        task=request.form["task"]
        if not task:
            return redirect('/tasks')
        conn.execute("INSERT INTO tasktable(title,completed) VALUES (?,?)", (task, 0))
        conn.commit()
    tasks=conn.execute("SELECT *FROM tasktable").fetchall()
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

@app.route('/api/student')
def student():
    return {
        "name": "Your Name",
    "college": "Madan Bhandari",
    "course": "BSc CSIT"
    }

if __name__ == '__main__':
    app.run(debug=True)
