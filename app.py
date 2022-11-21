import os
from helper import db

from flask import Flask, render_template, redirect, request, flash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
cur = db.cursor()

class User(UserMixin):
    def __init__(self, id, username, password):
         self.id = id
         self.username = username
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id

@login_manager.user_loader
def load_user(ID):
   cur = db.cursor()
   cur.execute("SELECT * from users where ID = ?;",[ID])
   cur = cur.fetchone()
   if cur is None:
      return None
   else:
      return User(int(cur[0]), cur[1], cur[2])

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = "hello_pat"

@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=['GET', 'POST'])
def index():
    # Primary we have to check if user is currently logged 
    index = request.form.get("task_index")
    if current_user.is_authenticated:
        # We get tuple of our tasks
        if request.form.get("task"):
            task = request.form.get("task")
            if task:
                cur.execute("INSERT INTO tasks (task, userID, type) VALUES(?, ?, ?);", (task, current_user.id, "PLAIN"))
                db.commit()
            tasks = cur.execute("SELECT task, ID FROM tasks WHERE userID = ? AND type = 'PLAIN' ORDER BY ID DESC;", (current_user.id,)).fetchall()
            return render_template("index.html", tasks=tasks)

        # If user finished the task we change location of it
        elif request.form.get("finish"):
            cur.execute("UPDATE tasks SET type = 'FINISHED' WHERE ID = ?;", [index])
            db.commit()
            tasks = cur.execute("SELECT task, ID FROM tasks WHERE userID = ? AND type = 'PLAIN' ORDER BY ID DESC;", [current_user.id]).fetchall()
            return render_template("index.html", tasks=tasks)

        # If user deleter task we remove it from our database
        elif request.form.get("delete"):
            cur.execute("DELETE FROM tasks WHERE ID = ?", [index])
            db.commit()
            tasks = cur.execute("SELECT task, ID FROM tasks WHERE userID = ? AND type = 'PLAIN' ORDER BY ID DESC;", [current_user.id]).fetchall()
            return render_template("index.html", tasks=tasks)

        else:
            tasks = cur.execute("SELECT task, ID FROM tasks WHERE userID = ? AND type = 'PLAIN' ORDER BY ID DESC;", [current_user.id]).fetchall()
            return render_template("index.html", tasks=tasks)
    else:
        return render_template("index.html")

@app.route("/finished")
def finished():
    tasks = cur.execute("SELECT task, ID FROM tasks WHERE userID = ? AND type = 'FINISHED' ORDER BY ID DESC;", [current_user.id]).fetchall()
    return render_template("finished.html", tasks=tasks)

@app.route("/login", methods=["GET", "POST"])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username must be provided")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password must be provided")
            return render_template("login.html")
        # Query database for username
        rows = cur.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")]).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], (request.form.get("password"))):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in; second '0' in our tuple represents ID
        user = rows[0]
        us = load_user(user[0])
        login_user(us)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    
    # Register user
    
    if request.method == "POST":

        # Check if username is not blank and is not in database

        username = request.form.get("username")
        password = request.form.get("password")
        if not username or len(cur.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchall()) == 1:
            flash("Incorrect username or it's already in usage")
            return render_template("register.html")
        elif not password or password != request.form.get("confirmation"):
            flash("Incorrect password or they don't match")
            return render_template("register.html")

        # When everything is correct, we get username and hash password
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        # We store new registrant for our database
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?);", (username, hash))
        db.commit()

        # We redirect user for index
        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    
    # Log user out
    logout_user()
    # Redirect user to login form
    return redirect("/")


