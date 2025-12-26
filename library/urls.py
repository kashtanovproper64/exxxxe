from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для автоматической генерации URL
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    # Традиционные URL для книг и авторов
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/new/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('authors/', views.AuthorListCreateView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyView.as_view(), name='author_detail'),
    
    # DRF ViewSet URL для задач (To-Do)
    # Генерируемые маршруты:
    # GET/POST /tasks/ - список/создание задач
    # GET/PUT/PATCH/DELETE /tasks/{id}/ - получение/обновление/удаление конкретной задачи
    path('', include(router.urls)),
]
