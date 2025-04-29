from django.db import models
from django.contrib.auth.models import User

# Клас статті — описує структуру однієї статті в блозі
class Article(models.Model):
    title = models.CharField(max_length=200)  # Заголовок статті
    slug = models.SlugField(unique=True)      # Унікальний слаг для URL (наприклад: /blog/my-post)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор статті — зв'язок із користувачем
    content = models.TextField()              # Основний текст статті
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення (встановлюється автоматично)
    updated_at = models.DateTimeField(auto_now=True)      # Дата останнього редагування (оновлюється автоматично)
    
    # Вибір статусу статті
    STATUS_CHOICES = [
        ('draft', 'Чернетка'),
        ('published', 'Опублікована'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # Статус статті

    def __str__(self):
        return self.title  # Як буде відображатись стаття у адмінці чи консолі