import requests
import sys

def check_api_key(name: str, api_key: str):
    """
    Проверяет правильность API ключа для указанного имени.
    :param name: Имя для API ключа (например, ключевое имя).
    :param api_key: API ключ, который нужно проверить.
    """
    try:
        # Отправка запроса на сервер с API ключом и именем
        response = requests.post(
            "https://long-time.ru/api/verify.php",  # Адрес API для проверки
            json={"key_name": name, "key": api_key},  # Передаем key_name и key отдельно
            timeout=5
        )

        # Выводим статус ответа
        print(f"HTTP Статус ответа: {response.status_code}")
        print(f"Ответ от сервера: {response.text}")

        # Преобразуем ответ в формат JSON
        data = response.json()

        # Проверяем, что сервер вернул данные
        if not data:
            print("Ответ от сервера пустой.")
            sys.exit(1)

        print(f"Ответ от сервера (JSON): {data}")

        # Проверяем, валиден ли ключ
        if data.get("valid") and data.get("valid") == True:
            print(f"API ключ для '{name}' валиден.")
        else:
            print("Не правильный API ключ.")
            sys.exit(1)  # Завершаем выполнение программы, если ключ невалиден

    except Exception as e:
        print(f"Не удалось подключиться к серверу для проверки API ключа: {e}")
        sys.exit(1)  # Завершаем выполнение программы в случае ошибки соединения
