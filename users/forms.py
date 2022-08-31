from django import forms
# 直接使用 Django 内置的用户模型
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        required=True,
        min_length=3,
        max_length=20,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        min_length=3,
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username']
