def get_user_input() -> str:
    """
    Display the menu options and get the user's choice.

    Returns:
        str: The user's choice from the menu.
    """
    print("\nВыберите действие:")
    print("1. Поиск фильмов по ключевому слову")
    print("2. Поиск фильмов по жанру и году")
    print("3. Поиск фильмов по актёру")
    print("4. Поиск фильмов по рейтингу")
    print("5. Показать популярные запросы")
    print("6. Выход")
    return input("Ваш выбор: ")


def display_results(results: list, result_type: str) -> None:
    """
    Display search results in the terminal.

    Args:
        results (list): A list of dictionaries containing search results.
        result_type (str): The type of search performed (e.g., "keyword", "actor", "genre_year", "rating").
    """
    if not results:
        print(f"Нет результатов для запроса: {result_type}")
        return

    print("\nРезультаты поиска:")
    for film in results:
        if result_type == "keyword" or result_type == "actor":
            print(f"ID: {film['film_id']}, Название: {film['title']}, Год: {film['release_year']}")
        elif result_type == "genre_year":
            print(f"ID: {film['film_id']}, Название: {film['title']}, Год: {film['release_year']}, Жанр: {film['genre']}")
        elif result_type == "rating":
            print(f"ID: {film['film_id']}, Название: {film['title']}, Год: {film['release_year']}, Рейтинг: {film['rating']}")
