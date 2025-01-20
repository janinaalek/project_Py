from db import (
    connect,
    ensure_search_logs_table,
    search_by_keyword,
    search_by_genre_and_year,
    search_by_actor,
    search_by_rating,
    save_search_log,
    get_popular_searches,
)
from user_interface import get_user_input, display_results


def main() -> None:
    """
    Main function to run the interactive movie search application.
    """
    connection = connect()  # Establish a single database connection
    ensure_search_logs_table(connection)  # Ensure the logs table exists

    try:
        while True:
            choice = get_user_input()

            if choice == '1':
                keyword = input("Введите ключевое слово: ")
                results = search_by_keyword(connection, keyword)
                save_search_log(connection, keyword, "keyword")
                display_results(results, "keyword")

            elif choice == '2':
                genre = input("Введите жанр: ")
                try:
                    year = int(input("Введите год: "))
                    results = search_by_genre_and_year(connection, genre, year)
                    save_search_log(connection, f"{genre}, {year}", "genre_year")
                    display_results(results, "genre_year")
                except ValueError:
                    print("Некорректный ввод года. Попробуйте снова.")

            elif choice == '3':
                actor_name = input("Введите имя актёра: ")
                results = search_by_actor(connection, actor_name)
                save_search_log(connection, actor_name, "actor")
                display_results(results, "actor")

            elif choice == '4':
                print("\nДоступные категории рейтинга: G, PG, PG-13, R, NC-17")
                rating = input("Введите категорию рейтинга: ").strip().upper()
                results = search_by_rating(connection, rating)
                save_search_log(connection, rating, "rating")
                display_results(results, "rating")

            elif choice == '5':
                # Show the most popular search queries
                popular_searches = get_popular_searches(connection)
                if popular_searches:
                    print("\nПопулярные запросы:")
                    for search in popular_searches:
                        print(f"Запрос: {search['search_term']}, Частота: {search['frequency']}")
                else:
                    print("Популярных запросов пока нет.")

            elif choice == '6':
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор, попробуйте снова.")
    finally:
        connection.close()  # Close the database connection when done


if __name__ == "__main__":
    main()
