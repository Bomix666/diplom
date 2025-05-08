from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        help_text="Обязательное поле. Только буквы, цифры и символы @/./+/-/_",
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Минимум 8 символов. Не используйте слишком простой пароль.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Введите пароль ещё раз для подтверждения.",
    )

    class Meta:
        model = User
        fields = ("username",)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'avatar', 'balance', 'department']
        labels = {
            'phone': 'Телефон',
            'birth_date': 'Дата рождения',
            'avatar': 'Аватар',
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        } 