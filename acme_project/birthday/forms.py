# birthday/forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Birthday
from .validators import real_age

# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = ('first_name', 'last_name', 'birthday', 'image')
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birthday': 'Дата рождения',
            'image': 'Фото'
        }
        help_texts = {
            'last_name': 'Необязательное поле'
        }

    def clean_first_name(self):
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам
        # и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):
        # Вызов родительского метода clean.
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )
