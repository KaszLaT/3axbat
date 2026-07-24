
***

```markdown
3axbat, (use pip install 3axbat)


![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![PyPI](https://img.shields.io/pypi/v/3axbat.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Status](https://img.shields.io/badge/status-active--development-orange.svg)

Неофициальная, высокооптимизированная Python-обертка для API Blockman Go. 

`3axbat` автоматически обрабатывает сложный протокол аутентификации `x-sign` в игре. Путем реверс-инжиниринга алгоритма подписи официального Android-клиента, эта библиотека позволяет разработчикам бесшовно взаимодействовать с приватным API Blockman Go, автоматически управляя RSA-шифрованием паролей, ротацией API-ключей и MD5-подписью запросов под капотом.

## Возможности

- **Автоматическая аутентификация:** Бесшовно обрабатывает RSA-шифрование пароля и генерацию заголовков `xsign` / `xnonce` / `xtime`.
- **Ротация API-ключей:** Автоматически циклически меняет валидные пары API-ключей для обхода лимитов и избежания обнаружения.
- **Управление устройствами:** Получает и ротирует валидные ID устройств и подписи, чтобы гарантировать прием запросов шлюзом.
- **Чистый объектно-ориентированный дизайн:** Забудьте о грязных сырых HTTP-запросах. Взаимодействуйте с API через чистые методы и классы данных.
- **Управление сессиями:** Встроенная обработка сессий для быстрых последовательных запросов.

## Установка

Вы можете установить `3axbat` напрямую из PyPI:

```bash
pip install 3axbat
```

## Быстрый старт

> **Примечание:** Из-за соглашений об именовании в Python (имена модулей не могут начинаться с цифры), пакет в PyPI называется `3axbat`, но импортируется как `axbat`.

```python
from axbat import Client, AuthenticationError

def main():
    # Инициализация клиента
    client = Client()
    
    # Вход с использованием ваших данных Blockman Go
    try:
        client.login("your_username", "your_password")
        print("[+] Вход выполнен успешно!")
    except AuthenticationError as e:
        print(f"[-] Ошибка входа: {e}")
        return

    # Получение данных профиля
    profile = client.get_profile()
    print(f"Вы вошли как: {profile.nickname} (ID: {profile.user_id})")
    print(f"Уровень: {profile.level} | VIP: {profile.vip_level}")
    
    # Получение списка друзей
    friends = client.get_friends()
    print(f"\nУ вас {len(friends)} друзей:")
    for friend in friends[:5]:
        print(f"  - {friend.nickname} [{friend.status_text}]")
        
    # Получение IP игрового сервера (например, Bed Wars)
    server = client.get_game_server(1008)
    print(f"\nIP:Port сервера Bed Wars: {server}")

if __name__ == "__main__":
    main()
```

## Доступные методы

### Client
- `client.login(username, password)` - Аутентифицируется на шлюзе и получает токен доступа.
- `client.get_profile(user_id=None)` - Получает данные профиля. Если `user_id` не указан, получает профиль вошедшего пользователя.
- `client.set_nickname(name)` - Изменяет никнейм аккаунта.
- `client.set_description(text)` - Обновляет описание профиля (макс. 80 символов).
- `client.get_friends()` - Возвращает список объектов `Friend` с их статусом онлайн.
- `client.send_friend_request(user_id, game_type=None)` - Отправляет заявку в друзья.
- `client.get_game_server(game_type)` - Аутентифицируется на сервере диспетчеризации игр и возвращает строку `IP:Port`.

## Технические детали

Blockman Go защищает свой API-шлюз (`gw.sandboxol.com`) с помощью кастомного протокола подписи запросов. Каждый запрос требует:
1. API Key (`x-apikey`) и Secret Key.
2. Случайный 32-символьный nonce (`xnonce`).
3. Unix timestamp (`xtime`).
4. MD5-хеш (`xsign`), объединяющий API-ключ, путь эндпоинта, nonce, timestamp, отсортированные параметры, тело запроса и секретный ключ.
5. Если пользователь авторизован, второй MD5-хеш, добавляющий ID устройства.

`3axbat` полностью абстрагирует этот процесс. Библиотека извлекает валидные API-ключи и использует тот же самый RSA публичный ключ, что и официальный клиент, для шифрования пароля перед передачей.

## Отказ от ответственности

Использование этого проекта осуществляется на ваш собственный риск. Библиотека не аффилирована, не одобрена и не связана с Blockman Go или GVERSE INTERNATIONAL PTE. LTD. Разработчики `3axbat` не несут ответственности за любой ущерб или блокировку аккаунтов, которые могут возникнуть в результате использования данной библиотеки.

## Лицензия

Этот проект лицензирован под лицензией MIT — подробности см. в файле [LICENSE](LICENSE).
```