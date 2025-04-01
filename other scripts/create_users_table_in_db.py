import pymysql
from pymysql import MySQLError

def create_tables():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='Anshuman@0812',  # Replace with your MySQL password
            database='movies_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()

        tables = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "user_saved_movies": """
                CREATE TABLE IF NOT EXISTS user_saved_movies (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    movie_id INT,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
                )
            """,
            "user_searched_movies": """
                CREATE TABLE IF NOT EXISTS user_searched_movies (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    movie_id INT,
                    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
                )
            """
        }
        
        for table_name, table_query in tables.items():
            cursor.execute(table_query)
            print(f"Table '{table_name}' created successfully!")

        connection.commit()  # Commit changes to DB
    
    except MySQLError as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    create_tables()
