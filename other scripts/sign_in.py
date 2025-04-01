from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import pymysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import requests

app = Flask(__name__)
app.secret_key = "b'\x9f\x1a\x8c\x7e\x3d\x2b\x4f\x5e\x6a\x7c\x8d\x9e\xaf\xbc\xcd\xde'"

bcrypt = Bcrypt(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# MySQL connection function
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Anshuman@0812',
        db='movies_db',
        cursorclass=pymysql.cursors.DictCursor
    )

# User Model for Flask-Login
class User(UserMixin):
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(id=user_data['id'], email=user_data['email'], name=user_data['name'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(id=user_data['id'], email=user_data['email'], name=user_data['name'])
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid user. New user? Register [here]", "danger")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except:
            flash("Email already exists. Try logging in.", "danger")
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
