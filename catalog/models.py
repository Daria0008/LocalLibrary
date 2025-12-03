import uuid

from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    """Хранение жанров книг"""

    name = models.CharField(
        max_length=200,
        help_text="Введите название жанра"
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """Абстрактное описание книги в базе"""

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',
                               on_delete=models.SET_NULL,
                               null=True)
    summary = models.TextField(max_length=1000,
                               help_text="Опишите краткое содержание книги")
    isbn = models.CharField('ISBN',
                            max_length=13,
                            help_text="13 символов")
    genre = models.ManyToManyField(Genre,
                                   help_text="Выберите жанр книги")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Создает небольшую выборку по жанрам
        для отображения в админке
        """

        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True

        return False
    
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Описание экземпляра книги"""

    LOAN_STATUS = (
        ('m', 'На реставрации'),
        ('o', 'На руках'),
        ('a', 'В наличии'),
        ('r', 'Забронирована'),
    )

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text="Уникальный числовой идентификатор для книги")
    borrower = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    book = models.ForeignKey('Book',
                             on_delete=models.SET_NULL,
                             null=True)    
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='m',
                              help_text="Метка наличия")
    
    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f"Книга рег.номер {self.id} под названием {self.book.title}"


class Author(models.Model):
    """Модель для сведений об авторе"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])    

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        ordering = ['last_name']


class Language(models.Model):
    """Языки для книг"""

    name = models.CharField(max_length=100,
                            unique=True,
                            help_text="Укажите язык текста")    

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])
    
    def __str__(self):
        return f"Язык текста {self.name}"
