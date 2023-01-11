from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
from django.utils.translation import gettext
from django.utils.translation import ngettext


class LoginForm(AuthenticationForm):
    user_name = gettext("Имя пользователя")
    password_trs = gettext("Пароль")
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': user_name
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': password_trs
    }))


class RegistrationForm(UserCreationForm):
    password_trs1 = gettext("Пароль")
    password_trs2 = gettext("Подтвердите пароль")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': password_trs1
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': password_trs2
    }))

    class Meta:
        user_name2 = gettext('Имя пользователя')
        email_str = gettext('Почта')
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': user_name2

            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': email_str
            })
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш отзыв...'
            })
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        your_email = gettext('Ваше почта...')
        your_name = gettext('Ваше имя...')
        model = Customer
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': your_email
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': your_email
            })
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        data1 = gettext('Ваш город...')
        data2 = gettext('Ваш район...')
        data3 = gettext('Ваш адрес...')
        data4 = gettext('Ваш номер телефона...')

        model = ShippingAddress
        fields = ['city',  'state', 'address', 'phone']

        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': data1
            }),

            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': data2
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': data3
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': data4
            })
        }
