from flask import Flask, render_template, request
import json 

app = Flask(__name__)

with open("tasks.json", "r") as file:
    taskl=json.load(file)
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
        taskl.append(task)    
        with open("tasks.json", "w") as file:
            json.dump(taskl, file)
    return render_template('tasks.html', tasks=taskl)

if __name__ == '__main__':
    app.run(debug=True)
