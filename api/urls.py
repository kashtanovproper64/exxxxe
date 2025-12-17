from django.urls import path
from .views import AuthorListCreateAPIView, AuthorRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('authors/', AuthorListCreateAPIView.as_view(), name='author_list_create'),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroyAPIView.as_view(), name='author_detail_update_delete'),
]
