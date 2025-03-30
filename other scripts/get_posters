import os
import requests
import pymysql
from imdb import IMDb

# Initialize IMDb object
ia = IMDb()

# Folder to save posters
SAVE_DIR = "movie_posters"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_db_connection():
    return pymysql.connect(
        host = 'localhost',
        user = "root",
        password = "Anshuman@0812",
        database = "movies_db"
    )

conn = get_db_connection()
cursor = conn.cursor()

# extract all titles from the database
cursor.execute("SELECT title FROM movies")
movie_titles = cursor.fetchall()

movie_titles = [title[0] for title in movie_titles]

# movie_titles = ["Avatar"]

def download_poster(movie_title):
    """Fetch and download movie poster from IMDb"""
    try:
        movies = ia.search_movie(movie_title)
        if not movies:
            print(f"❌ Movie not found: {movie_title}")
            return

        movie = ia.get_movie(movies[0].movieID)
        poster_url = movie.get("full-size cover url")  # Get full-size poster URL

        if not poster_url:
            print(f"❌ No poster found for: {movie_title}")
            return

        # Download image
        response = requests.get(poster_url)
        if response.status_code == 200:
            file_name = os.path.join(SAVE_DIR, f"{movie_title}.jpg")
            with open(file_name, "wb") as img_file:
                img_file.write(response.content)
            print(f"✅ Downloaded: {movie_title}")

            # Insert poster details into the database
            cursor.execute(
                "UPDATE movies SET poster_path = %s WHERE title = %s",
                (f"movie_posters/{movie_title}.jpg", movie_title)
            )
            conn.commit()

        else:
            print(f"❌ Failed to download: {movie_title}")

    except Exception as e:
        print(f"⚠️ Error processing {movie_title}: {e}")

# Process all movies
for title in movie_titles:
    download_poster(title)

print("\n🎉 All posters downloaded!")
