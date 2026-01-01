# Server Time API

Простое тестовое приложение на FastAPI, которое возвращает текущее время сервера.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

Запустите сервер командой:
```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: http://localhost:8000

## Endpoints

- **GET /** - Информация об API
- **GET /time** - Получить текущее время сервера
- **GET /health** - Проверка здоровья сервера
- **GET /docs** - Интерактивная документация Swagger UI
- **GET /redoc** - Альтернативная документация ReDoc

## Пример использования

```bash
curl http://localhost:8000/time
```

Ответ:
```json
{
  "server_time": "2026-01-01T12:30:45.123456",
  "timestamp": 1735734645.123456
}
```

## Docker

### Сборка образа:
```bash
docker build -t server-time-api .
```

### Запуск контейнера:
```bash
docker run -d -p 8000:8000 --name time-api server-time-api
```

### Остановка контейнера:
```bash
docker stop time-api
docker rm time-api
```

## Особенности

- ✅ Асинхронные эндпоинты
- ✅ Автоматическая документация API
- ✅ Валидация данных с помощью Pydantic
- ✅ Health check endpoint
- ✅ Форматированное время (ISO 8601) и Unix timestamp
- ✅ Docker поддержка
