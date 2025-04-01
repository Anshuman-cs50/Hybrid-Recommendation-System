from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)

# import import_ipynb
# from movie_recommendation_system_with_basic_concept import Recommend_Movies_with_BOW

# Database configuration (update with your credentials)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'raGed2025@off'
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

def Recommend_movie_to_user(user_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch user preferences or history from the database
            cursor.execute("""
                            select title from movies where movie_id in
                            (select movie_id from user_saved_movies where user_id = %s);
                        """, (user_id,))
            user_preferences = [movie[0] for movie in cursor.fetchall()]
            
            if user_preferences:
                # Call your recommendation function here
                recommended_movies = tuple()
                for movie in user_preferences:
                    recommended_movies += Recommend_Movies_with_BOW(movie)
                return recommended_movies
            else:
                return []
    finally:
        connection.close()

@app.route('/api/movies')
def get_movies():
    if session.get('user_id') is None:
        return render_template('login.html')

    # This is where you'll implement your database queries
    # Sample structure - replace with actual database queries
    movies = {
        "latest": [],
        "popular": [],
        "action": [],
        "Recommended": [],
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

            # movies['Recommended'] = Recommend_Movies_to_user(session['user_id'])

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


@app.route('/search')
def search_movies():
    search_query = request.args.get('q', '')
    connection = get_db_connection()
    
    movies = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM movies 
                WHERE title LIKE %s
                ORDER BY release_date DESC
                LIMIT 20
            """, ('%' + search_query + '%',))
            movies = cursor.fetchall()
        connection.close()
    except Exception as e:
        print(f"Search error: {e}")
    
    return render_template('search_results.html', 
                         movies=movies, 
                         query=search_query)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    connection = get_db_connection()
    movie = None
    try:
        with connection.cursor() as cursor:
            # Get movie details
            cursor.execute("""
                SELECT * FROM movies 
                WHERE movie_id = %s
            """, (movie_id,))
            movie = cursor.fetchone()
            
            # Get genres
            if movie:
                cursor.execute("""
                    SELECT g.name 
                    FROM genres g
                    JOIN movie_genres mg ON g.id = mg.genre_id
                    WHERE mg.movie_id = %s
                """, (movie_id,))
                genres = cursor.fetchall()
                movie['genres'] = [g['name'] for g in genres]
            
        connection.close()
    except Exception as e:
        print(f"Movie details error: {e}")
    
    if not movie:
        return render_template('404.html'), 404
    
    return render_template('movie_detail.html', movie=movie)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users (username, password) 
                        VALUES (%s, %s)
                    """, (username, password))
                    connection.commit()
                    session['user_id'] = cursor.lastrowid
                connection.close()
                return render_template('index.html')
            except Exception as e:
                print(f"Login error: {e}")
                connection.rollback()
                connection.close()
        else:
            return render_template('login.html', error="All fields are required.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if username and email and password:
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users (username, email, password) 
                        VALUES (%s, %s, %s)
                    """, (username, email, password))
                    connection.commit()
                    session['user_id'] = cursor.lastrowid
                connection.close()
                return render_template('login.html')
            except Exception as e:
                print(f"Registration error: {e}")
                connection.rollback()
                connection.close()
        else:
            return render_template('register.html', error="All fields are required.")
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
