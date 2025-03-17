from flask import Flask, render_template, session, request, flash, redirect
from __main__ import app
import sqlite3
import hashlib
import user_routes

@app.route("/")
def Home():
    user = session.get('user')
    return render_template("index.html", user=user)

@app.route("/sign-up", methods=["GET", "POST"])
def SignUp():
    user = session.get('user')
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    if request.method == "POST":
        email = request.form["email"]
        first_name = request.form["first_name"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        #Searches the database for a email matching the email the user entered into the form.
        query = cur.execute("SELECT * FROM users WHERE user_email = (?)", [email])
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        #Sign up input validation
        if len(email) < 4: #if email is shorter than 4 characters
            flash('Email must be greater than 3 characters!', category='error') #pop-up alert to incorrect email lenght
        elif len(first_name) < 3: #if firstName is shorter than 2 characters in lenght
            flash('First name must be greater than 2 characters!', category='error') #pop-up alert to incorrect first name lenght
        elif len(phone) != 11:
            flash("Phone number is invalid!") #if phone number is shorter than 11 characters an error message will be shown
        elif password != confirm_password: #if password1 is not equal to password2
            flash('Passwords must be the same!', category='error') #pop-up alert to inconsistent password entries
        elif len(password) < 7: #if password1 is less than 7 characters
            flash('Password must be atleast 7 characters!', category='error') #pop-up alert to incorrect password lenght
        elif query.fetchall() != []: #Checks if the email was found in the database.
            flash("Account on this email already exists!", category="error")
        else: #if there's nothing wrong with input, add user to the database
            #add user to database
            flash('Account Created!', category='success')
            query = cur.execute("INSERT INTO users(user_email, user_first_name, user_phone, user_password) VALUES(?,?,?,?)", [email, first_name, phone, hashedPassword])
        db.commit()
        db.close()
    return render_template("sign_up.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def Login():
    user = session.get('user')
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        query = cur.execute("SELECT * FROM users WHERE user_email = (?) AND user_password = (?) ", [email, hashedPassword])
        result = query.fetchone()
        if result == None:
            flash("Incorrect email or password!", category="error")
        else:
            flash("Successful Login", category="ssuccess")
            user = session['user'] = [result[0], result[1], result[2], result[3]]
            return redirect("/")#User redirected to homepage
    return render_template("login.html", user=user)

@app.route("/reset-password", methods=["GET", "POST"])
def Reset():
    user = session.get('user')
   #Further development would have the reset password functioning
    return render_template("reset_password.html", user=user)