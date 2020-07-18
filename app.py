from flask import Flask, render_template, request, redirect, session, flash
# , flash, jsonify, session
# from flask_session import Session
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Forget any user_id
    # session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username", 403)
            return redirect ('/login')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", 403)
            return redirect ('/login')

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        username = rows[0]['username']

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password", 403)
            return redirect ('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash('You were successfully logged in')
        # Redirect user to home page
        return redirect("/account")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')    


if __name__ == '__main__':
    app.debug = True
    app.run()