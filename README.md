# Автотесты API сервиса «Яндекс Самокат»

Проект автотестов для учебного API-сервиса Яндекс Самокат (аренда самокатов). Покрыты ручки работы с курьерами и заказами. Тесты написаны на Python с использованием `pytest` и `requests`, отчётность — Allure.

Тестируемый стенд: `https://qa-scooter.praktikum-services.ru`

---

## Стек

| Инструмент | Назначение |
|---|---|
| Python 3.11+ | Язык написания тестов |
| pytest | Фреймворк запуска тестов |
| requests | HTTP-клиент для запросов к API |
| Faker | Генерация уникальных тестовых данных |
| Allure | Формирование отчётов о прогоне |

---

## Структура проекта

```
.
├── conftest.py               # Общие фикстуры (api_client, сервисы, создание/удаление данных)
├── requirements.txt          # Зависимости проекта
├── pytest.ini                # Конфигурация pytest
├── data/
│   ├── __init__.py
│   ├── urls.py               # URL-константы ручек и BASE_URL
│   ├── messages.py           # Ожидаемые сообщения об ошибках
│   └── generators.py         # Генераторы тестовых данных (Faker)
├── services/
│   ├── __init__.py
│   ├── courier_service.py     # Методы ручек курьеров
│   └── order_service.py       # Методы ручек заказов
├── tests/
│   ├── __init__.py
│   ├── test_create_courier.py
│   ├── test_login_courier.py
│   ├── test_create_order.py
│   ├── test_get_orders_list.py
│   ├── test_delete_courier.py
│   ├── test_accept_order.py
│   └── test_get_order_by_track.py
└── utils/
    ├── __init__.py
    └── api_client.py          # Обёртка над requests.Session (timeout, retry, Allure-аттачи)
```

---

## Установка

```bash
# 1. Клонировать репозиторий
git clone <URL_РЕПОЗИТОРИЯ>
cd <НАЗВАНИЕ_ПАПКИ>

# 2. Создать и активировать виртуальное окружение
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt
```

---

## Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest tests/test_create_courier.py

# Конкретный тест
pytest tests/test_create_courier.py::TestCreateCourier::test_create_courier_when_valid_data_returns_201_and_ok_true

# По маркеру (пример)
pytest -m courier

# Подробный вывод
pytest -v
```

---

## Отчёт Allure

```bash
# 1. Прогон тестов с сохранением результатов
pytest --alluredir=allure-results --clean-alluredir

# 2. Сгенерировать HTML-отчёт
allure generate allure-results -o allure-report --clean

# 3. Открыть отчёт в браузере
allure open allure-report

# Либо посмотреть результаты без генерации HTML
allure serve allure-results
```

> Для генерации отчёта требуется установленный Allure CLI.
> Скачать: https://github.com/allure-framework/allure2/releases

---

## Покрытые сценарии

### Курьеры

| Ручка | Метод | Тесты |
|---|---|---|
| Создание курьера | `POST /api/v1/courier` | Успешное создание, дубликат логина, отсутствие обязательных полей |
| Логин курьера | `POST /api/v1/courier/login` | Успешный вход, неверный логин/пароль, отсутствие полей, несуществующий пользователь |
| Удаление курьера | `DELETE /api/v1/courier/{id}` | Успешное удаление, без id, несуществующий id, повторное удаление |

### Заказы

| Ручка | Метод | Тесты |
|---|---|---|
| Создание заказа | `POST /api/v1/orders` | Параметризация по цвету: BLACK, GREY, оба, без цвета; проверка `track` |
| Список заказов | `GET /api/v1/orders` | Возврат списка заказов |
| Приём заказа | `PUT /api/v1/orders/accept/{id}` | Успешный приём, отсутствие/неверный courierId, отсутствие/неверный order_id |
| Получить заказ по треку | `GET /api/v1/orders/track` | Успешный запрос, без номера, несуществующий заказ |

---

## Особенности реализации

### Работа с параметрами вместо тела запроса

В документации сервиса есть неточность: для ручек отмены и приёма заказа `id` передаётся **в query-параметрах**, а не в теле запроса. Проект учитывает это:

```python
# Отмена заказа — track в параметрах
self.client.put(urls.ORDERS_CANCEL_PATH, params={"track": track})

# Приём заказа — courierId в параметрах, id заказа в пути
path = urls.ORDERS_ACCEPT_PATH.format(order_id=order_id)
self.client.put(path, params={"courierId": courier_id})
```

### Управление тестовыми данными

Тестовые данные создаются и удаляются через фикстуры с `yield` — очистка выполняется даже при падении проверки:

- `registered_courier` — регистрирует курьера, удаляет после теста;
- `created_courier` — создаёт и авторизует курьера, удаляет после теста;
- `created_order` — создаёт заказ, закрывает его после теста (завершает принятый заказ либо отменяет новый);
- `accepted_order` — создаёт и принимает заказ, завершает и удаляет курьера после теста.

### Уникальность данных

Логины курьеров формируются через `uuid4`, что исключает коллизии между тестами и при повторных прогонах.

### Устойчивость к нагрузке стенда

`ApiClient` настроен на `timeout=30` секунд и автоматические повторы при сетевых сбоях и ответах `5xx`, что снижает число ложных падений на учебном стенде.

---

## Дополнительно

- Тесты независимы друг от друга и не используют общие изменяемые данные.
- Проверяются и код ответа, и тело ответа.
- Для каждого теста задан читаемый `allure.title`.

---

## Возможные вопросы

**Тесты падают с `ReadTimeout`.** Учебный стенд может отвечать медленно. Повторный запуск обычно решает проблему:

```bash
pytest
```

**`allure: command not found`.** Не установлен Allure CLI — см. раздел «Отчёт Allure».

**Как добавить новый тест.** Создайте метод в классе соответствующего файла в `tests/`, используйте фикстуры из `conftest.py` и константы из `data/urls.py`. Пути к ручкам не пишите строками — берите из `urls.py`.