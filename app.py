import os
from flask import Flask,redirect, render_template, request, session, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import sqlexecute, login_required, httperror
from algorithm.kmeans import kmeans

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET, POST"])
def index():
    """Main page: user can execute an iteration"""
    
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("index.html")

@app.route("/exec_kmeans", methods="POST")
def exec_kmeans():
    """Execute algorithm and return with results"""
    
    selected_scenario = request.form.get("scenario")
    selected_k_amount = request.form.get("k_amount")
    selected_max_iter = request.form.get("max_iter")
    
    # Ensure user selected scenario
    if not selected_scenario:
        return httperror("Must select a scenario", 400)
    
    # Ensure user's selected scenario is valid
    if selected_scenario not in ["scenario1","scenario2","scenario3","scenario4","scenario5"]:
        return httperror("Select a valid scenario", 400)
    
    # Check if user typed k_amount
    if not selected_k_amount:
        selected_k_amount = 4
    
    # Check if amount is not between 1 and 20
    if not 20 >= selected_k_amount >= 1:
        return httperror("K amount range is between 1 and 20", 400)
    
    # Check if user typed max_iter
    if not selected_max_iter:
        selected_max_iter = 20
    
    kmeans(scenario=selected_scenario, k=selected_k_amount, max_iter=selected_max_iter)

    return render_template()


@app.route("/executions")
@login_required
def executions():
    return render_template("executions.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """User can change his password"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("account.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        new_password = request.form.get("new_password")
        new_password_confirmation = request.form.get("new_password_confirmation")

        # Ensure user typed new password
        if not new_password:
            return httperror("must provide new password", 400)

        # Ensure user typed confirmation
        if not new_password_confirmation:
            return httperror("must confirm new password", 400)

        # Ensure new password and its confirmation match
        if new_password != new_password_confirmation:
            return httperror("passwords don't match", 400)

        # Change hash in user row
        new_hash_password = generate_password_hash(new_password)

        user_in_session = session.get("user_id")

        sqlexecute(
            "UPDATE users SET hash = ? WHERE id = ?", new_hash_password, user_in_session
        )

        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return httperror("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return httperror("must provide password", 403)

        # Query database for username
        rows = sqlexecute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return httperror("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return httperror("must provide username", 400)

        # Ensure password was submitted
        if not password:
            return httperror("must provide password", 400)

        # Ensure password confirmation was submitted
        if not confirmation:
            return httperror("must confirm password", 400)

        # Confirming the passwords
        if confirmation != password:
            return httperror("passwords don't match", 400)

        hash_password = generate_password_hash(password)

        # Check if the username already exists
        try:
            sqlexecute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hash_password,
            )
        except ValueError:
            return httperror("user already exists", 400)

        # Log in new user
        new_user = sqlexecute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = new_user[0]["id"]

        return redirect("/")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
    )