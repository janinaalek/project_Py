import pymysql
from typing import List, Dict

# Function to connect to the database
def connect() -> pymysql.connections.Connection:
    """
    Establish a connection to the database.
    """
    return pymysql.connect(
        host='ich-edit.edu.itcareerhub.de',
        user='ich1',
        password='ich1_password_ilovedbs',
        database='050824_AYV_sakila',
        cursorclass=pymysql.cursors.DictCursor
    )

# Search for movies by a keyword
def search_by_keyword(keyword: str) -> List[Dict]:
    query = """
    SELECT film_id, title, description, release_year 
    FROM film 
    WHERE title LIKE %s OR description LIKE %s 
    LIMIT 10;
    """
    with connect().cursor() as cursor:
        cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        return cursor.fetchall()

# Search for movies by genre and year
def search_by_genre_and_year(genre: str, year: int) -> List[Dict]:
    query = """
    SELECT f.film_id, f.title, f.description, f.release_year, c.name AS genre
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s AND f.release_year = %s
    LIMIT 10;
    """
    with connect().cursor() as cursor:
        cursor.execute(query, (genre, year))
        return cursor.fetchall()

# Search for movies by actor
def search_by_actor(actor_name: str) -> List[Dict]:
    query = """
    SELECT f.film_id, f.title, f.description, f.release_year
    FROM film f
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id
    WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
    LIMIT 10;
    """
    with connect().cursor() as cursor:
        cursor.execute(query, (f'%{actor_name}%',))
        return cursor.fetchall()

# Search for movies by rating
def search_by_rating(rating: str) -> List[Dict]:
    """
    Search for movies by a specific rating category (e.g., G, PG, PG-13, R, NC-17).
    """
    query = """
    SELECT film_id, title, description, release_year, rating
    FROM film
    WHERE rating = %s
    LIMIT 10;
    """
    with connect().cursor() as cursor:
        cursor.execute(query, (rating,))
        return cursor.fetchall()

# Save a search log to the database
def save_search_log(search_term: str, search_type: str) -> None:
    query = """
    INSERT INTO search_logs (search_term, search_type)
    VALUES (%s, %s);
    """
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(query, (search_term, search_type))
        connection.commit()
    except Exception as e:
        print(f"Error saving log: {e}")
    finally:
        connection.close()

# Get the most popular search queries
def get_popular_searches() -> List[Dict]:
    query = """
    SELECT search_term, COUNT(*) AS frequency 
    FROM search_logs 
    GROUP BY search_term 
    ORDER BY frequency DESC 
    LIMIT 10;
    """
    with connect().cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

# Ensure the search_logs table exists
def ensure_search_logs_table() -> None:
    query = """
    CREATE TABLE IF NOT EXISTS search_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        search_term VARCHAR(255),
        search_type VARCHAR(50),
        search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
    except Exception as e:
        print(f"Error ensuring table exists: {e}")
    finally:
        connection.close()
