from rest_framework import serializers
from .models import Author, Task

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    # Получаем отображаемые названия для choices
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title', 
            'description', 
            'due_date', 
            'priority', 
            'status', 
            'created_at',
            'priority_display',
            'status_display'
        ]
        read_only_fields = ['id', 'created_at', 'priority_display', 'status_display']
    
    def validate_title(self, value):
        """Проверяем, что заголовок не пустой"""
        if not value or not value.strip():
            raise serializers.ValidationError("Заголовок не может быть пустым")
        return value.strip()
    
    def validate_priority(self, value):
        """Проверяем, что приоритет из допустимых значений"""
        valid_priorities = ['HIGH', 'MEDIUM', 'LOW']
        if value not in valid_priorities:
            raise serializers.ValidationError(f"Приоритет должен быть одним из: {valid_priorities}")
        return value
    
    def validate_status(self, value):
        """Проверяем, что статус из допустимых значений"""
        valid_statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Статус должен быть одним из: {valid_statuses}")
        return value
