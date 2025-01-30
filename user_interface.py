def get_user_input() -> str:
    """
    Display the menu options and get the user's choice.

    Returns:
        str: The user's choice from the menu.
    """
    menu_options = [
        "Поиск фильмов по ключевому слову",
        "Поиск фильмов по жанру и году",
        "Поиск фильмов по актёру",
        "Поиск фильмов по рейтингу",
        "Показать популярные запросы",
        "Выход"
    ]

    print("\nВыберите действие:")
    for index, option in enumerate(menu_options, start=1):
        print(f"{index}. {option}")

    return input("Ваш выбор: ")

def display_results(results: list, result_type: str) -> None:
    """Display search results in the terminal."""
    if not results:
        print(f"Нет результатов для запроса: {result_type}")
        return

    print("\nРезультаты поиска:")
    for film in results:
        film_info = [f"ID: {film['film_id']}", f"Название: {film['title']}", f"Год: {film['release_year']}"]
        if result_type == "genre_year":
            film_info.append(f"Жанр: {film['genre']}")
        elif result_type == "rating":
            film_info.append(f"Рейтинг: {film['rating']}")
        print(", ".join(film_info))
