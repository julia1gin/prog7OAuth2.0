from requests_oauthlib import OAuth2Session
import os
import sys

# 1. Настройка: Получение учетных данных и URL-ов
# CLIENT_ID и CLIENT_SECRET читаются из переменных окружения
# $env:CLIENT_ID="ВАШ_ID"

CLIENT_ID = "Ov23li30pQ81Dbx5vJOE"
CLIENT_SECRET = "8079729ad9cfa30575887663a2f4dbe2797ed579"
REDIRECT_URI = "https://localhost:8000/callback"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Проверка, что секреты установлены
if not CLIENT_ID or not CLIENT_SECRET:
    print("Ошибка: CLIENT_ID или CLIENT_SECRET не установлены как переменные окружения.")
    print("Установите их перед запуском скрипта.")
    sys.exit(1)

# URL-ы для GitHub API
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
RESOURCE_URL = "https://api.github.com/user"
SCOPE = ["read:user"]  # Запрашиваемые права доступа

# 2. Шаг: Запрос кода авторизации
print("--- Шаг 1: Получение кода авторизации ---")
# Создаем сессию OAuth, которая будет управлять процессом
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)

# Формируем URL для перенаправления пользователя
authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)

# Сохраняем state для проверки CSRF-атаки (хотя requests-oauthlib делает это внутренне)
# Для этого примера просто выводим его
print(f"Сгенерированное состояние (state): {state}")
print("Перейдите по этой ссылке в браузере для авторизации:")
print(authorization_url)

# 3. Шаг: Обмен кода на Access Token
print("\n--- Шаг 2: Обмен кода на Access Token ---")
# Ожидаем, пока пользователь авторизуется и будет перенаправлен
redirect_response = input("Вставьте полный URL перенаправления из браузера (включая 'code' и 'state'): ")

try:
    # Обмениваем код авторизации на Access Token
    token = oauth.fetch_token(
        TOKEN_URL,
        authorization_response=redirect_response,
        client_secret=CLIENT_SECRET
    )

    print("\nУспешно получен Access Token и другие токены:")
    print(token)

except Exception as e:
    print(f"\nОшибка при обмене кода на токен: {e}")
    sys.exit(1)

# 4. Шаг: Доступ к защищенному ресурсу
print("\n--- Шаг 3: Доступ к защищенному ресурсу ---")
# Используем сессию 'oauth', в которую уже встроен полученный токен
# requests-oauthlib автоматически добавит заголовок: Authorization: Bearer <Access Token>
try:
    r = oauth.get(RESOURCE_URL)

    print(f"Статус ответа Resource Server: {r.status_code}")

    if r.status_code == 200:
        print("Ваши данные пользователя GitHub (первые 5 ключей):")
        data = r.json()
        for key in list(data.keys())[:5]:
            print(f"- {key}: {data[key]}")
    else:
        print(f"Ошибка при доступе к ресурсу. Ответ сервера: {r.text}")

except Exception as e:
    print(f"Произошла ошибка при запросе к ресурсу: {e}")