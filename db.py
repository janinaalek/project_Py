import pymysql
import os
import logging
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def connect() -> pymysql.connections.Connection:
    """Establish a connection to the MySQL database using environment variables."""
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info("✅ Successfully connected to the database.")
        return connection
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database connection error: {e}")
        raise

def ensure_search_logs_table(connection: pymysql.connections.Connection) -> None:
    """Ensure that the 'search_logs' table exists in the database."""
    query = """
    CREATE TABLE IF NOT EXISTS search_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        search_term VARCHAR(255),
        search_type VARCHAR(50),
        search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
        logging.info("✅ Checked or created 'search_logs' table.")
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error ensuring search_logs table: {e}")
        raise

def get_available_genres(connection: pymysql.connections.Connection) -> List[str]:
    """Retrieve available genres from the category table."""
    query = "SELECT name FROM category;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return [row['name'] for row in cursor.fetchall()]
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error retrieving genres: {e}")
        return []

def get_available_ratings(connection: pymysql.connections.Connection) -> List[str]:
    """Retrieve available ratings from the film table."""
    query = "SELECT DISTINCT rating FROM film;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return [row['rating'] for row in cursor.fetchall()]
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error retrieving ratings: {e}")
        return []

def search_by_keyword(connection: pymysql.connections.Connection, keyword: str) -> List[Dict]:
    """Search for movies by a keyword in the title or description."""
    query = """
    SELECT film_id, title, description, release_year 
    FROM film 
    WHERE title LIKE %s OR description LIKE %s 
    LIMIT 10;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
            results = cursor.fetchall()
            logging.info(f"🔍 Keyword search executed successfully: {keyword}")
            return results
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error executing keyword search: {e}")
        return []

def search_by_genre_and_year(connection: pymysql.connections.Connection, genre: str, year: int) -> List[Dict]:
    """Search for movies by genre and release year."""
    query = """
    SELECT f.film_id, f.title, f.description, f.release_year, c.name AS genre
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s AND f.release_year = %s
    LIMIT 10;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (genre, year))
            results = cursor.fetchall()
            logging.info(f"🔍 Genre & Year search executed: {genre}, {year}")
            return results
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error executing genre & year search: {e}")
        return []

def search_by_actor(connection: pymysql.connections.Connection, actor_name: str) -> List[Dict]:
    """Search for movies featuring a specific actor."""
    query = """
    SELECT f.film_id, f.title, f.description, f.release_year
    FROM film f
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id
    WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
    LIMIT 10;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (f'%{actor_name}%',))
            results = cursor.fetchall()
            logging.info(f"🔍 Actor search executed: {actor_name}")
            return results
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error executing actor search: {e}")
        return []

def search_by_rating(connection: pymysql.connections.Connection, rating: str) -> List[Dict]:
    """Search for movies by a specific rating category."""
    query = """
    SELECT film_id, title, description, release_year, rating
    FROM film
    WHERE rating = %s
    LIMIT 10;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (rating,))
            results = cursor.fetchall()
            logging.info(f"🔍 Rating search executed: {rating}")
            return results
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error executing rating search: {e}")
        return []

def save_search_log(connection: pymysql.connections.Connection, search_term: str, search_type: str) -> None:
    """Save a search log to the database."""
    query = """
    INSERT INTO search_logs (search_term, search_type)
    VALUES (%s, %s);
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (search_term, search_type))
        connection.commit()
        logging.info(f"✅ Search log saved: {search_term} ({search_type})")
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error saving search log: {e}")

def get_popular_searches(connection: pymysql.connections.Connection) -> List[Dict]:
    """
    Retrieve the most popular search queries.

    Args:
        connection (pymysql.connections.Connection): The active database connection.

    Returns:
        List[Dict]: A list of popular search queries with their frequency.
    """
    query = """
    SELECT search_term, COUNT(*) AS frequency 
    FROM search_logs 
    GROUP BY search_term 
    ORDER BY frequency DESC 
    LIMIT 10;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            logging.info(" Successfully retrieved popular search queries.")
            return results
    except pymysql.MySQLError as e:
        logging.error(f"❌ Error retrieving popular searches: {e}")
        return []

