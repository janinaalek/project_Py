import pymysql
from typing import List, Dict

def connect() -> pymysql.connections.Connection:
    """
    Establish a connection to the MySQL database.

    Returns:
        pymysql.connections.Connection: The database connection object.
    """
    return pymysql.connect(
        host='ich-edit.edu.itcareerhub.de',
        user='ich1',
        password='ich1_password_ilovedbs',
        database='050824_AYV_sakila',
        cursorclass=pymysql.cursors.DictCursor
    )


def search_by_keyword(connection: pymysql.connections.Connection, keyword: str) -> List[Dict]:
    """
    Search for movies by a keyword in the title or description.

    Args:
        connection (pymysql.connections.Connection): The active database connection.
        keyword (str): The keyword to search for.

    Returns:
        List[Dict]: A list of movies matching the keyword.
    """
    query = """
    SELECT film_id, title, description, release_year 
    FROM film 
    WHERE title LIKE %s OR description LIKE %s 
    LIMIT 10;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        return cursor.fetchall()


def search_by_genre_and_year(connection: pymysql.connections.Connection, genre: str, year: int) -> List[Dict]:
    """
    Search for movies by genre and release year.

    Args:
        connection (pymysql.connections.Connection): The active database connection.
        genre (str): The genre to search for.
        year (int): The release year to search for.

    Returns:
        List[Dict]: A list of movies matching the genre and year.
    """
    query = """
    SELECT f.film_id, f.title, f.description, f.release_year, c.name AS genre
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s AND f.release_year = %s
    LIMIT 10;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (genre, year))
        return cursor.fetchall()


def search_by_actor(connection: pymysql.connections.Connection, actor_name: str) -> List[Dict]:
    """
    Search for movies featuring a specific actor.

    Args:
        connection (pymysql.connections.Connection): The active database connection.
        actor_name (str): The name of the actor.

    Returns:
        List[Dict]: A list of movies featuring the specified actor.
    """
    query = """
    SELECT f.film_id, f.title, f.description, f.release_year
    FROM film f
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id
    WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
    LIMIT 10;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (f'%{actor_name}%',))
        return cursor.fetchall()


def search_by_rating(connection: pymysql.connections.Connection, rating: str) -> List[Dict]:
    """
    Search for movies by a specific rating category.

    Args:
        connection (pymysql.connections.Connection): The active database connection.
        rating (str): The rating category (e.g., G, PG, PG-13, R, NC-17).

    Returns:
        List[Dict]: A list of movies matching the rating category.
    """
    query = """
    SELECT film_id, title, description, release_year, rating
    FROM film
    WHERE rating = %s
    LIMIT 10;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (rating,))
        return cursor.fetchall()


def save_search_log(connection: pymysql.connections.Connection, search_term: str, search_type: str) -> None:
    """
    Save a search log to the database.

    Args:
        connection (pymysql.connections.Connection): The active database connection.
        search_term (str): The term that was searched.
        search_type (str): The type of search performed (e.g., keyword, genre_year, actor, rating).
    """
    query = """
    INSERT INTO search_logs (search_term, search_type)
    VALUES (%s, %s);
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (search_term, search_type))
    connection.commit()


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
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def ensure_search_logs_table(connection: pymysql.connections.Connection) -> None:
    """
    Ensure that the 'search_logs' table exists in the database.

    Args:
        connection (pymysql.connections.Connection): The active database connection.
    """
    query = """
    CREATE TABLE IF NOT EXISTS search_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        search_term VARCHAR(255),
        search_type VARCHAR(50),
        search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()
