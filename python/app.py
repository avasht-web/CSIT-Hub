from flask import Flask, render_template, request
import json 
import sqlite3
app=Flask(__name__)
with open("tasks.json", "r") as file:
    taskl=json.load(file)
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
    if request.method=="POST":
        task=request.form["task"]
        conn=database()
        conn.execute("INSERT INTO tasktable(title,completed) VALUES (?,?)", (task, 0))
        conn.commit() 
        conn.close()
       
        taskl.append(task)
           
        with open("tasks.json", "w") as file:
            json.dump(taskl, file)
    return render_template('tasks.html', tasks=taskl)
@app.route('/api/student')
def student():
    return {
        "name": "Your Name",
    "college": "Madan Bhandari",
    "course": "BSc CSIT"
    }
if __name__ == '__main__':
    app.run(debug=True)
