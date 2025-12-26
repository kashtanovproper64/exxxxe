from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from .models import Book, Author, Task
from .serializers import AuthorSerializer, TaskSerializer
from .forms import BookForm

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = '/books/'

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = '/books/'

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = '/books/'

class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления задачами (To-Do) с полным CRUD функционалом.
    
    Поддерживает:
    - Создание задач с различными приоритетами и статусами
    - Обновление статуса через PATCH запросы
    - Сортировку по приоритету и дате создания
    - Удаление задач
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Переопределяем queryset для настройки сортировки:
        1. По приоритету (HIGH -> MEDIUM -> LOW)
        2. По дате создания (новые сверху)
        """
        return Task.objects.all().order_by(
            '-priority',  # Высокий приоритет сверху
            '-created_at'  # Новые задачи сверху
        )
    
    def perform_create(self, serializer):
        """
        Автоматически устанавливаем значения по умолчанию при создании
        """
        serializer.save(
            priority='MEDIUM',  # По умолчанию средний приоритет
            status='PENDING'    # По умолчанию ожидает
        )
    
    def get_serializer_context(self):
        """
        Передаем request в контекст сериализатора для расширенной функциональности
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
