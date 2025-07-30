# birthday/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Birthday, Congratulation
from .validators import real_age

# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        exclude = ('author',)
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
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=(
                    f'{first_name} {last_name} пытался опубликовать запись!'
                ),
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form) 


class CongratulationForm(forms.ModelForm):

    class Meta:
        model = Congratulation
        fields = ('text',)
