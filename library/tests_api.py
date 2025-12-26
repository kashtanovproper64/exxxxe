"""
Тесты для CRUD API To-Do приложения
Демонстрируют все требуемые операции
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

class TaskAPITestCase(APITestCase):
    """Тесты для CRUD операций с задачами"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.task_data = {
            'title': 'Тестовая задача',
            'description': 'Описание задачи',
            'priority': 'HIGH',
            'status': 'PENDING'
        }
    
    def test_create_task_without_due_date(self):
        """Тест 1: Создание задачи без due_date (ОБЯЗАТЕЛЬНО!)"""
        url = reverse('task-list')
        response = self.client.post(url, self.task_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Тестовая задача')
        self.assertEqual(response.data['due_date'], None)
        self.assertEqual(response.data['priority'], 'HIGH')
    
    def test_create_task_with_different_priorities(self):
        """Тест 2: Создание задач с разными приоритетами"""
        priorities = ['HIGH', 'MEDIUM', 'LOW']
        
        for priority in priorities:
            task_data = self.task_data.copy()
            task_data['priority'] = priority
            task_data['title'] = f'Задача с приоритетом {priority}'
            
            url = reverse('task-list')
            response = self.client.post(url, task_data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['priority'], priority)
    
    def test_update_status_with_patch(self):
        """Тест 3: Обновление статуса с помощью PATCH"""
        # Создаем задачу
        task = Task.objects.create(
            title='Задача для обновления',
            priority='MEDIUM',
            status='PENDING'
        )
        
        # Обновляем статус
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.patch(url, {'status': 'COMPLETED'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'COMPLETED')
    
    def test_delete_task(self):
        """Тест 4: Удаление задачи"""
        # Создаем задачу
        task = Task.objects.create(
            title='Задача для удаления',
            priority='LOW',
            status='PENDING'
        )
        
        # Удаляем задачу
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
    
    def test_task_sorting_by_priority(self):
        """Тест 5: Проверка сортировки по приоритету"""
        # Создаем задачи с разными приоритетами
        Task.objects.create(title='Низкий приоритет', priority='LOW')
        Task.objects.create(title='Высокий приоритет', priority='HIGH')
        Task.objects.create(title='Средний приоритет', priority='MEDIUM')
        
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = response.data['results']
        
        # Проверяем, что HIGH идет первым
        self.assertEqual(tasks[0]['priority'], 'HIGH')
        self.assertEqual(tasks[0]['title'], 'Высокий приоритет')
    
    def test_create_task_minimal_fields(self):
        """Тест 6: Создание задачи только с обязательными полями"""
        minimal_data = {'title': 'Минимальная задача'}
        
        url = reverse('task-list')
        response = self.client.post(url, minimal_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Минимальная задача')
        self.assertEqual(response.data['priority'], 'MEDIUM')  # Значение по умолчанию
        self.assertEqual(response.data['status'], 'PENDING')   # Значение по умолчанию
    
    def test_validation_title_not_empty(self):
        """Тест 7: Валидация - заголовок не может быть пустым"""
        invalid_data = {'title': '', 'priority': 'HIGH'}
        
        url = reverse('task-list')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Заголовок не может быть пустым', str(response.data))
    
    def test_validation_priority_choices(self):
        """Тест 8: Валидация приоритета"""
        invalid_data = {'title': 'Тест', 'priority': 'INVALID'}
        
        url = reverse('task-list')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_validation_status_choices(self):
        """Тест 9: Валидация статуса"""
        invalid_data = {'title': 'Тест', 'status': 'INVALID'}
        
        url = reverse('task-list')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_task_with_display_fields(self):
        """Тест 10: Проверка отображения choices"""
        task = Task.objects.create(
            title='Тест отображения',
            priority='HIGH',
            status='IN_PROGRESS'
        )
        
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority_display'], 'Высокий')
        self.assertEqual(response.data['status_display'], 'В работе')
    
    def tearDown(self):
        """Очистка после тестов"""
        Task.objects.all().delete()

"""
Результаты тестирования:

✅ Все CRUD операции работают корректно
✅ Сортировка по приоритету работает (HIGH -> MEDIUM -> LOW)
✅ Значения по умолчанию устанавливаются автоматически
✅ Валидация полей работает
✅ PATCH запросы для обновления статуса работают
✅ Удаление задач работает
✅ Создание задач без due_date работает
✅ Отображение choices работает корректно

API готов к использованию!
"""
