from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager, PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError('Enter Email!!')
        user=self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    

class Users(AbstractBaseUser,PermissionsMixin):
    username= models.CharField(max_length = 255)
    email = models.EmailField(max_length= 255,unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'users'


    def __str__(self) -> str:
        return self.email
    
