from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm, PasswordResetForm,
    SetPasswordForm, AuthenticationForm
)
from .models import User
from dogs.mixins import StyleFormMixin


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    agree = forms.BooleanField(
        label='Я согласен с политикой конфиденциальности',
        required=True,
        error_messages={'required': 'Необходимо согласиться с политикой конфиденциальности'}
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'agree']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Минимум 8 символов'
        self.fields['agree'].widget.attrs['class'] = 'form-check-input'


class ProfileUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'avatar', 'bio', 'birth_date']


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))


class CustomPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass


class CustomSetPasswordForm(StyleFormMixin, SetPasswordForm):
    pass