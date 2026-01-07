from google_auth_oauthlib.flow import Flow
import json

# Имя файла, который вы скачали из Google Cloud Console
CLIENT_SECRET_FILE = './client_secret.json'

# Scope: Доступ только для чтения к библиотеке Google Фото (как в статье)
# Примечание: В реальной работе вы используете scope для того API, к которому хотите получить доступ
SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary.readonly',
]

# Настройка потока
flow = Flow.from_client_secrets_file(
    CLIENT_SECRET_FILE,
    scopes=SCOPES,
)

# Установка Redirect URI (должен совпадать с тем, что в Cloud Console)
flow.redirect_uri = 'https://localhost:8080/auth/google/callback'

# Генерируем URL авторизации.
# access_type='offline' - это КЛЮЧЕВОЙ параметр, который запрашивает refresh token.
authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
)

print("--- Шаг 1: Запрос кода авторизации ---")
print('1. Перейдите по этой ссылке, чтобы авторизовать доступ:')
print(authorization_url)

print("\n--- Шаг 2: Ввод кода ---")
# Ожидаем, пока пользователь авторизуется
authorization_response = input('2. Вставьте полный URL перенаправления из браузера (с параметрами code и state): ')

try:
    # Обмен кода на токены
    flow.fetch_token(authorization_response=authorization_response)

    # Получаем учетные данные и конвертируем их в JSON для вывода
    credentials_json = flow.credentials.to_json()

    print("\nУспешно получены токены:")
    print(json.dumps(json.loads(credentials_json), indent=2))

    # Сохраняем refresh token для дальнейшего использования
    print("\nRefresh Token успешно получен и готов к использованию для обновления Access Token.")

except Exception as e:
    print(f"\nОшибка при обмене кода на токен: {e}")