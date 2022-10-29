from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager
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
    
    

class User(AbstractBaseUser):
    username= models.CharField(max_length = 255)
    email = models.EmailField(max_length= 255,unique=True)


    USERNAME_FIELDS = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
