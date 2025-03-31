import import_ipynb
# import movie_recommendation_system_with_basic_concept as mr

from flask import Flask, jsonify, render_template
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
movies = {"genres": {}}  # Initialize with a dictionary for genres

cursor.execute("""
                SELECT name FROM genres
               """)

genres = [genre[0] for genre in cursor.fetchall()]

for genre in genres:
    cursor.execute("""
                    SELECT m.*
                    FROM movies m
                    JOIN movie_genres mg ON m.movie_id = mg.movie_id
                    JOIN genres g ON mg.genre_id = g.id
                    WHERE g.name = %s
                    ORDER BY m.popularity DESC 
                    LIMIT 2
                   """, (genre,))
    
    # Fetch the results
    mg = cursor.fetchall()
    
    # Convert to a list of dictionaries (if cursor.description is available)
    column_names = [desc[0] for desc in cursor.description]
    mg = [dict(zip(column_names, row)) for row in mg]

    movies["genres"][genre] = mg  # Assign list of dictionaries

print(movies["genres"].keys())




