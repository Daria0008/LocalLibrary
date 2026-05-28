import datetime
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import BookInstance


class RenewBookForm(ModelForm):

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Эта дата уже прошла'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Нельзя выдать более, чем на 4 недели'))

        return data
    
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Обновить срок возврата'),}
        help_texts = {'due_back': _('Новая дата в пределах 4 недель')}
