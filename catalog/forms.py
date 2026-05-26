import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        label="Обновить срок возврата",
        help_text="Новая дата в пределах 4 недель",
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Эта дата уже прошла'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Нельзя выдать более, чем на 4 недели'))

        return data
