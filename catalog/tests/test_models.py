from django.test import TestCase

from catalog.models import Author


class AuthorModelTest(TestCase):
    """Проверяем корректность созданных объектов Автора"""

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(
            first_name='Тестовый автор',
            last_name='Тестовый автор'
        )
        cls.author = Author.objects.get(id=1)

    def test_author_model_kirilian_labels(self):
        """Проверяем, что названия полей на кириллице"""

        first_name = self.author._meta.get_field(
            'first_name').verbose_name

        last_name = self.author._meta.get_field(
            'last_name').verbose_name

        date_of_birth = self.author._meta.get_field(
            'date_of_birth').verbose_name

        date_of_death = self.author._meta.get_field(
            'date_of_death').verbose_name

        self.assertEqual(first_name, 'Имя')
        self.assertEqual(last_name, 'Фамилия')
        self.assertEqual(date_of_birth, 'Дата рождения')
        self.assertEqual(date_of_death, 'Дата смерти')

    def test_created_object_name(self):
        """Проверяем созданный метод __str__"""

        created_object_name = "Тестовый автор Тестовый автор"
        self.assertEqual(created_object_name, str(self.author))

    def test_get_absolute_url(self):
        """Проверяем метод с выдачей стро"""

        self.assertEqual(
            self.author.get_absolute_url(),
            "/catalog/author/1"
        )
