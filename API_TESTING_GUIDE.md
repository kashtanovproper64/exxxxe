# Тестирование CRUD API для To-Do приложения

## Запуск сервера
```bash
cd /home/proper/Control-2
python manage.py runserver
```

## Доступные API эндпоинты

### Базовый URL
- API: `http://127.0.0.1:8000/library/tasks/`
- Админка: `http://127.0.0.1:8000/admin/`

## Тестовые сценарии

### 1. Создание задачи без due_date (обязательно!)
```bash
curl -X POST http://127.0.0.1:8000/library/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Изучить Django REST Framework",
    "description": "Прочитать документацию и создать первый API",
    "priority": "HIGH",
    "status": "IN_PROGRESS"
  }'
```

### 2. Создание задачи с высоким приоритетом
```bash
curl -X POST http://127.0.0.1:8000/library/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Подготовить презентацию",
    "description": "Создать слайды о проекте",
    "priority": "HIGH",
    "status": "PENDING"
  }'
```

### 3. Создание задачи с низким приоритетом
```bash
curl -X POST http://127.0.0.1:8000/library/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Прочитать книгу",
    "description": "Программирование на Python",
    "priority": "LOW",
    "status": "PENDING"
  }'
```

### 4. Получение списка всех задач (сортировка по приоритету)
```bash
curl -X GET http://127.0.0.1:8000/library/tasks/
```

### 5. Обновление статуса с помощью PATCH
```bash
# Получаем ID задачи из предыдущего запроса, предположим ID=1
curl -X PATCH http://127.0.0.1:8000/library/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "COMPLETED"
  }'
```

### 6. Удаление задачи
```bash
# Удаляем задачу с ID=1
curl -X DELETE http://127.0.0.1:8000/library/tasks/1/
```

### 7. Создание задачи только с обязательными полями
```bash
curl -X POST http://127.0.0.1:8000/library/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Минимальная задача"
  }'
```

## Ожидаемый результат

### Сортировка по приоритету:
1. **HIGH** - Высокий приоритет (красный)
2. **MEDIUM** - Средний приоритет (по умолчанию)  
3. **LOW** - Низкий приоритет (зеленый)

### Значения по умолчанию:
- `priority`: "MEDIUM"
- `status`: "PENDING"
- `created_at`: автоматически при создании

### Ответ API содержит:
```json
{
  "id": 1,
  "title": "Изучить Django REST Framework",
  "description": "Прочитать документацию и создать первый API",
  "due_date": null,
  "priority": "HIGH",
  "status": "IN_PROGRESS", 
  "created_at": "2024-01-15T10:30:00Z",
  "priority_display": "Высокий",
  "status_display": "В работе"
}
```

## Тестирование через браузер
Откройте `http://127.0.0.1:8000/library/tasks/` в браузере для интерактивного тестирования через DRF интерфейс.

## Валидация
- Заголовок не может быть пустым
- Приоритет должен быть: HIGH, MEDIUM, LOW
- Статус должен быть: PENDING, IN_PROGRESS, COMPLETED
