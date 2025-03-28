from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Anshuman@0812',
        database='movies_db'
    )

conn = get_db_connection()
cursor = conn.cursor()

@app.route('/')
def index():
    return "Welcome to the Movie Recommendation System!"

if __name__ == '__main__':
    app.run(debug=True)
