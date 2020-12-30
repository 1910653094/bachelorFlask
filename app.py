from datetime import datetime

from flask import Flask, request, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "bachelor_work"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bachelor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    complete = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id


db.create_all()


@app.route('/', methods=['POST', 'GET'])
def registration():
    error = None
    if request.method == 'POST':
        found_user = User.query.filter_by(username=request.form["username"]).first()
        if 'register' in request.form:
            if found_user:
                error = 'Username already exists'
            else:
                user = User(request.form["username"], request.form["password"])
                db.session.add(user)
                db.session.commit()
                session["user_id"] = user.id
                return redirect(url_for('tasks'))

        elif found_user and found_user.password == request.form["password"]:
            session["user_id"] = found_user.id
            return redirect(url_for('tasks'))

        else:
            error = 'Your username or password is wrong'

    return render_template("registration.html", error=error)


@app.route("/tasks", methods=['POST', 'GET'])
def tasks():
    user_id = session["user_id"]
    user_tasks = Task.query.filter_by(user_id=user_id)

    if request.method == 'POST':
        task = Task(request.form["title"], user_id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks'))

    return render_template('list.html', tasks=user_tasks, id=user_id)


@app.route("/update_task/<string:task_id>", methods=['POST', 'GET'])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()

    if request.method == 'POST':
        print(request.form["title"])
        task.title = request.form["title"]
        task.complete = "complete" in request.form
        db.session.commit()
        return redirect(url_for('tasks'))

    return render_template('update_task.html', task=task)


@app.route("/delete_task/<string:task_id>", methods=['POST', 'GET'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()

    if request.method == 'POST':
        if "confirm" in request.form:
            db.session.delete(task)
            db.session.commit()
        return redirect(url_for('tasks'))

    return render_template('delete.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
