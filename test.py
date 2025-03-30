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


def fetch_most_viewed_movies():
    cursor.execute("select movie_id, title, release_date, overview, poster_path from movies order by vote_count desc limit 2")
    most_viewed = cursor.fetchall()

    # Convert the result to a list of dictionaries
    most_viewed = [
        {
            'movie_id': row[0],
            'title': row[1],
            'release_date': row[2],
            'overview': row[3],
            'poster_path': row[4]
        } for row in most_viewed
    ]

    # helper function to fetch genres for a given movie_id
    def fetch_genres(movie_id):
        cursor.execute("""
                        select name from genres 
                        where id in (
                            select genre_id from movie_genres where movie_id = %s
                        )
                    """, (movie_id, ))
        genres = cursor.fetchall()
        return [genre[0] for genre in genres] # return a flatten list of genres

    # add attrifute genres to each movie in most_viewed
    for movie in most_viewed:
        movie["genres"] = fetch_genres(movie["movie_id"])

    return most_viewed

most_viewed = fetch_most_viewed_movies()
print(most_viewed)
