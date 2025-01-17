from db import (
    search_by_keyword,
    search_by_genre_and_year,
    search_by_actor,
    search_by_rating,
    save_search_log,
    get_popular_searches,
    ensure_search_logs_table,
)

# Main application loop
def main() -> None:
    """
    Main function to run the interactive movie search application.
    """
    # Ensure the 'search_logs' table exists
    ensure_search_logs_table()

    # Main loop for user interaction
    while True:
        print("\nВыберите действие:")
        print("1. Поиск фильмов по ключевому слову")
        print("2. Поиск фильмов по жанру и году")
        print("3. Поиск фильмов по актёру")
        print("4. Поиск фильмов по рейтингу")
        print("5. Показать популярные запросы")
        print("6. Выход")
        
        choice: str = input("Ваш выбор: ")
        
        if choice == '1':
            # Search for movies by keyword
            keyword: str = input("Введите ключевое слово: ")
            results = search_by_keyword(keyword)
            if results:
                save_search_log(keyword, "keyword")
                print("\nРезультаты поиска:")
                for film in results:
                    print(f"ID: {film['film_id']}, Название: {film['title']}, Год: {film['release_year']}")
            else:
                print("Фильмы с таким ключевым словом не найдены.")

        elif choice == '2':
            # Search for movies by genre and year
            genre: str = input("Введите жанр: ")
            try:
                year: int = int(input("Введите год: "))
                results = search_by_genre_and_year(genre, year)
                if results:
                    save_search_log(f"{genre}, {year}", "genre_year")
                    print("\nРезультаты поиска:")
                    for film in results:
                        print(f"ID: {film['film_id']}, Название: {film['title']}, Год: {film['release_year']}, Жанр: {film['genre']}")
                else:
                    print("Фильмы по указанным параметрам не найдены.")
            except ValueError:
                print("Некорректный ввод года. Попробуйте снова.")

        elif choice == '3':
            # Search for movies by actor
            actor_name: str = input("Введите имя актёра: ")
            results = search_by_actor(actor_name)
            if results:
                save_search_log(actor_name, "actor")
                print("\nРезультаты поиска:")
                for film in results:
                    print(f"ID: {film['film_id']}, Название: {film['title']}, Год: {film['release_year']}, Актёр: {actor_name}")
            else:
                print(f"Фильмы с участием актёра '{actor_name}' не найдены.")

        elif choice == '4':
            # Search for movies by rating
            print("\nДоступные категории рейтинга: G, PG, PG-13, R, NC-17")
            rating: str = input("Введите категорию рейтинга: ").strip().upper()
            results = search_by_rating(rating)
            if results:
                save_search_log(rating, "rating")
                print("\nРезультаты поиска:")
                for film in results:
                    print(f"ID: {film['film_id']}, Название: {film['title']}, Год: {film['release_year']}, Рейтинг: {film['rating']}")
            else:
                print(f"Фильмы с рейтингом '{rating}' не найдены.")

        elif choice == '5':
            # Show the most popular search queries
            popular_searches = get_popular_searches()
            if popular_searches:
                print("\nПопулярные запросы:")
                for search in popular_searches:
                    print(f"Запрос: {search['search_term']}, Частота: {search['frequency']}")
            else:
                print("Популярных запросов пока нет.")

        elif choice == '6':
            # Exit the program
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
