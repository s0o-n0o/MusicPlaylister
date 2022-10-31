from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserCreationForm,UserChangeForm
# Register your models here.

User = get_user_model()

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm #ユーザ編集画面で使うform
    add_form = UserCreationForm #ユーザ作成画面で使うform
#一覧画面で表示する
    list_display = ('username','email')
#ユーザ編集画面で表示する要素
    fieldsets = (
        ('ユーザ情報',{'fields':('usename','email','password')}),
    )

add_fieldsets = (
    ('ユーザ情報',{'fields':('usename',"email",'password','confirm_password')}),
)

admin.site.register(User,CustomizeUserAdmin)