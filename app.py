from flask import Flask, render_template, jsonify, request
import pymysql
from pymysql import Error

# import import_ipynb
# from movie_recommendation_system_with_basic_concept import Recommend_Movies_with_BOW, Recommend_Movies_with_TFIDF

app = Flask(__name__)

# Database configuration (update with your credentials)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Anshuman@0812'
app.config['MYSQL_DB'] = 'movies_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movies')
def get_movies():
    # This is where you'll implement your database queries
    # Sample structure - replace with actual database queries
    movies = {
        "latest": [],
        "popular": [],
        "action": []
    }
    
    try:
        # Example query structure (implement your actual queries here)
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Query for latest movies (you'll need to implement this)
            cursor.execute("""
                SELECT m.* 
                FROM movies m
                ORDER BY release_date DESC 
                LIMIT 10
            """)
            
            movies['latest'] = cursor.fetchall()

            # Query for popular movies
            cursor.execute("""
                SELECT m.* 
                FROM movies m
                ORDER BY popularity DESC 
                LIMIT 10
            """)
            movies['popular'] = cursor.fetchall()

            movies['Recommended'] = movies['popular']

            # Query for action movies
            cursor.execute("""
                SELECT m.* 
                FROM movies m
                JOIN movie_genres mg ON m.movie_id = mg.movie_id
                JOIN genres g ON mg.genre_id = g.id
                WHERE g.name = 'Action'
                LIMIT 10
            """)
            movies['action'] = cursor.fetchall()
        
        connection.close()
    except Exception as e:
        print(f"Database error: {e}")
    
    return jsonify(movies)

@app.route('/api/save_movie', methods=['POST'])
def save_movie_route():
    # This is where you'll implement the logic to save a movie
    user_id = request.form.get('user_id')
    movie_id = request.form.get('movie_id')

    if not user_id or not movie_id:
        return jsonify({"error": "User ID and Movie ID are required"}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if movie is already saved
        cursor.execute("""
            SELECT * FROM user_saved_movies WHERE user_id = %s AND movie_id = %s
        """, (user_id, movie_id))
        
        if cursor.fetchone():
            return jsonify({"message": "Movie already saved"}), 200

        # Insert into database
        cursor.execute("""
            INSERT INTO user_saved_movies (user_id, movie_id) VALUES (%s, %s)
        """, (user_id, movie_id))
        connection.commit()

        return jsonify({"message": "Movie saved successfully"}), 201
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)