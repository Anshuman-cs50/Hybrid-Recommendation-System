import pymysql
import pandas as pd
import json

# Database connection
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Anshuman@0812',
    database='movies_db'
)
cursor = conn.cursor()

# Creating tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT UNIQUE,
    title VARCHAR(255),
    release_date VARCHAR(20),
    overview TEXT,
    poster_path VARCHAR(255),
    budget BIGINT,
    revenue BIGINT,
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT,
    genre_id INT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE,
    UNIQUE KEY(movie_id, genre_id)
)
''')

# Load CSV data
data = pd.read_csv(r"Datasets/10000 Movies Data")
data.fillna("", inplace=True)

# Batch insert movies
movies_insert_query = '''
INSERT INTO movies (movie_id, title, release_date, overview, poster_path, budget, revenue, popularity, vote_average, vote_count)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    title = VALUES(title), 
    release_date = VALUES(release_date),
    overview = VALUES(overview),
    poster_path = VALUES(poster_path),
    budget = VALUES(budget),
    revenue = VALUES(revenue),
    popularity = VALUES(popularity),
    vote_average = VALUES(vote_average),
    vote_count = VALUES(vote_count)
'''

# Batch insert genres
genres_insert_query = "INSERT IGNORE INTO genres (name) VALUES (%s)"
movie_genre_insert_query = "INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)"

# Insert movies and genres
for _, row in data.iterrows():
    # Insert movie data
    cursor.execute(movies_insert_query, (
        row['Movie_id'],
        row['title'],
        row['release_date'],
        row['overview'],
        row['poster_path'],
        row['Budget'],
        row['Revenue'],
        row['popularity'],
        row['vote_average'],
        row['vote_count']
    ))

    # Handle genres robustly
    genres = row['Genres']
    
    # Normalize genre data format
    genre_list = []
    
    try:
        if genres.startswith("[") and genres.endswith("]"):
            # If it's a list of dictionaries (JSON-like string)
            genre_list = [g['name'] for g in json.loads(genres.replace("'", '"'))]
        elif genres.startswith("{") and genres.endswith("}"):
            # If it's a dictionary
            genre_dict = json.loads(genres.replace("'", '"'))
            genre_list = [v['name'] for v in genre_dict.values()]
        else:
            # If it's a comma-separated string
            genre_list = [g.strip() for g in genres.split(",")]
    except Exception as e:
        print(f"Error parsing genres for movie ID {row['Movie_id']}: {e}")
        continue

    # Insert genres and map them to movies
    for genre in genre_list:
        cursor.execute(genres_insert_query, (genre,))
        cursor.execute("SELECT id FROM genres WHERE name = %s", (genre,))
        genre_id = cursor.fetchone()[0]
        cursor.execute(movie_genre_insert_query, (row['Movie_id'], genre_id))

# Commit once after all inserts
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully!")
