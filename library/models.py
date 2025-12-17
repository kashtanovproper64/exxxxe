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
