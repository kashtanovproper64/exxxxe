from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.IntegerField()
    genres = models.CharField(max_length=500)  # Comma-separated genres
    co_authors = models.CharField(max_length=500, blank=True)  # Comma-separated co-authors
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    # Choices для приоритетов
    PRIORITY_CHOICES = [
        ('HIGH', 'Высокий'),
        ('MEDIUM', 'Средний'),
        ('LOW', 'Низкий'),
    ]
    
    # Choices для статусов
    STATUS_CHOICES = [
        ('PENDING', 'Ожидает'),
        ('IN_PROGRESS', 'В работе'),
        ('COMPLETED', 'Завершено'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    due_date = models.DateField(blank=True, null=True, verbose_name='Срок выполнения')
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='MEDIUM',
        verbose_name='Приоритет'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"
