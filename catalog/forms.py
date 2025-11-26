from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import UserBookStatus, BookInstance

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Введите дату возврата (до 4 недель от сегодня)",
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < date.today():
            raise ValidationError('Неверная дата - дата в прошлом')
        if data > (date.today() + timedelta(weeks=4)):
            raise ValidationError('Неверная дата - более чем через 4 недели')
        return data


class UserBookStatusForm(forms.ModelForm):
    class Meta:
        model = UserBookStatus
        fields = ['is_read', 'is_favorite']
        widgets = {
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }