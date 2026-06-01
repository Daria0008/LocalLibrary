from django.test import Client, TestCase

from forms import RenewBookForm


class RenewBookFormTest(TestCase):
    """Проверка работы формы"""

    @classmethod
    def setUpTestData(cls):
        cls.form = RenewBookForm()

    pass
