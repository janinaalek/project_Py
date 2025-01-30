import logging
from db import (
    connect,
    ensure_search_logs_table,
    search_by_keyword,
    search_by_genre_and_year,
    search_by_actor,
    search_by_rating,
    save_search_log,
    get_popular_searches,
    get_available_genres,
    get_available_ratings,
)
from user_interface import get_user_input, display_results

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main() -> None:
    """
    Main function to run the interactive movie search application.
    Establishes a database connection, ensures the logs table exists, and processes user input.
    """
    try:
        connection = connect()
        ensure_search_logs_table(connection)  # Ensure the search_logs table exists
    except Exception as e:
        logging.critical(f"❌ Database connection failed: {e}")
        print("❌ Ошибка: Не удалось подключиться к базе данных.")
        return

    try:
        while True:
            choice = get_user_input()

            if choice == '1':  #  Search by keyword
                keyword = input("Введите ключевое слово: ")
                results = search_by_keyword(connection, keyword)
                if results:
                    save_search_log(connection, keyword, "keyword")
                display_results(results, "keyword")

            elif choice == '2':  #  Search by genre and year (Dropdown menu)
                genres = get_available_genres(connection)
                if not genres:
                    print("❌ Ошибка: Жанры не загружены из базы данных.")
                    continue

                print("\nВыберите жанр из списка:")
                for i, genre in enumerate(genres, start=1):
                    print(f"{i}. {genre}")

                try:
                    genre_choice = int(input("Введите номер жанра: "))
                    if 1 <= genre_choice <= len(genres):
                        selected_genre = genres[genre_choice - 1]
                    else:
                        print("❌ Ошибка: Некорректный номер жанра.")
                        continue
                except ValueError:
                    print("❌ Ошибка: Введите число.")
                    continue

                year = input("Введите год: ")
                try:
                    year = int(year)
                    results = search_by_genre_and_year(connection, selected_genre, year)
                    if results:
                        save_search_log(connection, f"{selected_genre}, {year}", "genre_year")
                    display_results(results, "genre_year")
                except ValueError:
                    print("❌ Ошибка: Некорректный ввод года.")

            elif choice == '3':  #  Search by actor
                actor_name = input("Введите имя актёра: ")
                results = search_by_actor(connection, actor_name)
                if results:
                    save_search_log(connection, actor_name, "actor")
                display_results(results, "actor")

            elif choice == '4':  #  Search by rating (Dropdown menu)
                ratings = get_available_ratings(connection)
                if not ratings:
                    print("❌ Ошибка: Рейтинги не загружены из базы данных.")
                    continue

                print("\nВыберите рейтинг из списка:")
                for i, rating in enumerate(ratings, start=1):
                    print(f"{i}. {rating}")

                try:
                    rating_choice = int(input("Введите номер рейтинга: "))
                    if 1 <= rating_choice <= len(ratings):
                        selected_rating = ratings[rating_choice - 1]
                    else:
                        print("❌ Ошибка: Некорректный номер рейтинга.")
                        continue
                except ValueError:
                    print("❌ Ошибка: Введите число.")
                    continue

                results = search_by_rating(connection, selected_rating)
                if results:
                    save_search_log(connection, selected_rating, "rating")
                display_results(results, "rating")

            elif choice == '5':  #  Show popular searches
                results = get_popular_searches(connection)
                if results:
                    print("\nПопулярные запросы:")
                    for search in results:
                        print(f"Запрос: {search['search_term']}, Частота: {search['frequency']}")
                else:
                    print("Популярных запросов пока нет.")

            elif choice == '6':  #  Exit
                print("Выход из программы.")
                break

            else:
                print("❌ Ошибка: Неверный выбор, попробуйте снова.")

    finally:
        connection.close()
        logging.info(" Database connection closed.")

if __name__ == "__main__":
    main()
