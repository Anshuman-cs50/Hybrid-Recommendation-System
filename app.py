from flask import Flask, render_template, jsonify
import pymysql

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

if __name__ == '__main__':
    app.run(debug=True)