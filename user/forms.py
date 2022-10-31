from dataclasses import field
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model() #現在のアプリで使用しているモデルが返ってくる

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label = 'password',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label = 'password再入力',widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

    def clean(self):
        cleand_data = super().clean()
        password = cleand_data.get('password')
        confirm_password = cleand_data.get('comfirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
    
    def save(self,commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model= User
        fields = ('username','email','password')

    def clean_password(self):
        return self.initial['password'] #initial➡既に登録されている値を返す
