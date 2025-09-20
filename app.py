from flask import Flask, render_template, request, session, redirect, flash, url_for
import sqlite3
import re
import os
import pandas as pd
import pickle


app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('home.html')

# Create DB if not exists
def init_db():
    # Users DB
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

    # Questionnaire DB
    conn = sqlite3.connect("glowcare.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS new_user_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Age TEXT,
                    Gender TEXT,
                    SkinType TEXT,
                    Redness TEXT,
                    WaterIntake TEXT,
                    DietType TEXT,
                    SunExposure TEXT,
                    UsesSPF TEXT,
                    NaturalRemedyUsed TEXT,
                    CleanseFreq TEXT,
                    WashWaterTemp TEXT,
                    SleepHours TEXT,
                    StressFreq TEXT,
                    AwareOfVitaminE TEXT,
                    TriedDIY TEXT
                )''')
    conn.commit()
    conn.close()

# Call once
init_db()


    
@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/login')
def login_choice():
    return render_template('login.html')

# Placeholder routes for future development
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        # Password validation
        if len(password) < 8 or not re.search(r'[A-Z]', password) or \
           not re.search(r'[0-9]', password) or not re.search(r'[\W_]', password):
            message = "Password must be 8+ chars with uppercase, digit, and special character."
        elif password != confirm:
            message = "Passwords do not match."
        else:
            try:
                with sqlite3.connect('users.db') as conn:
                    c = conn.cursor()
                    # check if username already exists
                    c.execute("SELECT * FROM users WHERE username=?", (username,))
                    existing_user = c.fetchone()
                    if existing_user:
                        message = "❌ Username already exists. Please login."
                    else:
                        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                                  (username, email, password))
                        conn.commit()
                        return redirect('/loginnew')
            except sqlite3.IntegrityError:
                message = "❌ User already exists."

    return render_template("register.html", message=message)


@app.route("/loginnew", methods=["GET", "POST"])
def loginnew():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        row = c.fetchone()
        conn.close()

        if row:
            stored_password = row[0].strip()
            if stored_password == password:
                session["user"] = username
                return redirect("/are_you_ready")
            else:
                flash("❌ Incorrect password, please try again")
                return redirect("/loginnew")
        else:
            flash("❌ Username not found")
            return redirect("/loginnew")

    return render_template("loginnew.html")

    
import re

def is_valid_password(password):
    return (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

@app.route("/loginuser", methods=["GET", "POST"])
def loginuser():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/returning_user_questionnaire")
        else:
            flash("Invalid username or password")
            return redirect("/loginuser")

    return render_template("loginuser.html")

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            message = "Passwords do not match."
        elif not is_valid_password(new_password):
            message = "Password must be 8+ characters with uppercase, digit, and special character."
        else:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            if user:
                c.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
                conn.commit()
                conn.close()
                return redirect('/loginnew')
            else:
                message = "Email not found."

    return render_template('forgot_password.html', message=message)
    
@app.route("/are_you_ready", methods=["GET","POST"])
def are_you_ready():
    return render_template("are_you_ready.html")





# Ensure DB exists
def init_db():
    conn = sqlite3.connect("glowcare.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS new_user_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Age TEXT,
                    Gender TEXT,
                    SkinType TEXT,
                    Redness TEXT,
                    WaterIntake TEXT,
                    DietType TEXT,
                    SunExposure TEXT,
                    UsesSPF TEXT,
                    NaturalRemedyUsed TEXT,
                    CleanseFreq TEXT,
                    WashWaterTemp TEXT,
                    SleepHours TEXT,
                    StressFreq TEXT,
                    AwareOfVitaminE TEXT,
                    TriedDIY TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# Load trained models
new_user_morning_model = pickle.load(open("D:/MYPROJECT/new_user_morning_model.pkl", "rb"))
new_user_evening_model = pickle.load(open("D:/MYPROJECT/new_user_evening_model.pkl", "rb"))

def format_routine(routine, time_of_day):
    steps = routine.split(", ")

    # Ensure at least 3 items
    while len(steps) < 3:
        steps.append("suitable product")

    if time_of_day == "Morning":
        return f"Start your day by cleansing with a {steps[0].lower()}, then apply a {steps[1].lower()}, and finish with a {steps[2].lower()} to protect your skin."
    else:
        return f"Begin your evening by using a {steps[0].lower()}, follow with a {steps[1].lower()}, and complete your routine with a {steps[2].lower()} for overnight nourishment."

@app.route("/new_user_questionnaire", methods=["GET", "POST"])
def new_user_questionnaire():
    if request.method == "POST":
        form_data = {k: request.form[k] for k in request.form}

        # 🔹 Map form keys to dataset column names
        rename_map = {
            "Age": "Age",
            "Gender": "Gender",
            "Skin Type": "SkinType",
            "Redness or Inflammation": "Redness",
            "Water Intake": "WaterIntake",
            "Diet Type": "DietType",
            "Sun Exposure": "SunExposure",
            "Uses SPF": "UsesSPF",
            "Natural Remedies Used": "NaturalRemedyUsed",
            "Cleansing Frequency": "CleanseFreq",
            "Water Temperature": "WashWaterTemp",
            "Sleep Hours": "SleepHours",
            "Stress Frequency": "StressFreq",
            "Vitamin E Awareness": "AwareOfVitaminE",
            "Tried DIY Skincare Recently": "TriedDIY"
        }

        mapped_data = {rename_map[k]: v for k, v in form_data.items()}

        # Save to DB
        conn = sqlite3.connect("glowcare.db")
        c = conn.cursor()
        c.execute('''INSERT INTO new_user_responses (
                        Age, Gender, SkinType, Redness, WaterIntake, DietType,
                        SunExposure, UsesSPF, NaturalRemedyUsed, CleanseFreq,
                        WashWaterTemp, SleepHours, StressFreq, AwareOfVitaminE, TriedDIY
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  tuple(mapped_data.values()))
        conn.commit()
        conn.close()

        # 🔹 Prepare input
        input_df = pd.DataFrame([mapped_data])
        input_df_encoded = pd.get_dummies(input_df)

        # Align with morning model
        morning_cols = new_user_morning_model.feature_names_in_
        for col in morning_cols:
            if col not in input_df_encoded:
                input_df_encoded[col] = 0
        morning_input = input_df_encoded[morning_cols]

        # Align with evening model
        evening_cols = new_user_evening_model.feature_names_in_
        for col in evening_cols:
            if col not in input_df_encoded:
                input_df_encoded[col] = 0
        evening_input = input_df_encoded[evening_cols]

        # Predict
        morning_prediction = new_user_morning_model.predict(morning_input)[0]
        evening_prediction = new_user_evening_model.predict(evening_input)[0]

        # Format routines
        prediction = {
            "Morning Routine": format_routine(morning_prediction, "Morning"),
            "Evening Routine": format_routine(evening_prediction, "Evening")
        }

        return render_template(
            "results.html",
            morning_routine=prediction["Morning Routine"],
            evening_routine=prediction["Evening Routine"]
        )

    return render_template("new_user_questionnaire.html")





# Load returning user models
returning_morning_model = pickle.load(open("D:/MYPROJECT/returning_morning_model.pkl", "rb"))
returning_evening_model = pickle.load(open("D:/MYPROJECT/returning_evening_model.pkl", "rb"))

@app.route("/returning_user_questionnaire", methods=["GET", "POST"])
def returning_user_questionnaire():
    if request.method == "POST":
        form_data = {k: request.form[k] for k in request.form}

        # 🔹 Map form keys to dataset column names
        rename_map = {
            "follows_routine": "FollowsRoutine",
            "irritation": "Irritation",
            "skin_change": "SkinChange",
            "improvement": "Improvement",
            "new_diy": "TriedDIY"
        }
        mapped_data = {rename_map[k]: v for k, v in form_data.items()}

        # Save to DB (use original form keys if you want)
        conn = sqlite3.connect("glowcare.db")
        c = conn.cursor()
        c.execute('''INSERT INTO returning_user_responses
                     (username, follows_routine, irritation, skin_change, improvement, new_diy)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (session.get("user"),
                   form_data["follows_routine"],
                   form_data["irritation"],
                   form_data["skin_change"],
                   form_data["improvement"],
                   form_data["new_diy"]))
        conn.commit()
        conn.close()

        # 🔹 Prepare input for model with correct column names
        input_df = pd.DataFrame([mapped_data])
        input_df_encoded = pd.get_dummies(input_df)

        # Align with training columns
        model_cols = returning_morning_model.feature_names_in_
        for col in model_cols:
            if col not in input_df_encoded:
                input_df_encoded[col] = 0
        input_df_encoded = input_df_encoded[model_cols]
        print("DEBUG morning input:\n", input_df_encoded.head())
        morning_pred = returning_morning_model.predict(input_df_encoded)[0]
        print("DEBUG morning prediction:", morning_pred)

        evening_pred = returning_evening_model.predict(input_df_encoded)[0]
        print("DEBUG evening prediction:", evening_pred)

        print("DEBUG Encoded DataFrame:\n", input_df_encoded.head())

        # Predict
        morning_pred = returning_morning_model.predict(input_df_encoded)[0]
        evening_pred = returning_evening_model.predict(input_df_encoded)[0]

        # Format output
        morning_routine = format_routine(morning_pred, "Morning")
        evening_routine = format_routine(evening_pred, "Evening")

        return render_template("returning_results.html",
                               morning=morning_routine,
                               evening=evening_routine)

    return render_template("returning_user_questionnaire.html")

    return render_template("returning_user_questionnaire.html")

@app.route('/questionnaire')
def questionnaire():
    return "<h2>Questionnaire Coming Soon!</h2>"
  
if __name__ == '__main__':
    app.run(debug=True)
