from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    
    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError('Email is Required')
        
        if not password:
            raise ValueError('Password is Required')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class UserData(AbstractUser):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    channel_group = models.CharField(max_length=255)
    class Meta:
        unique_together = ('user', 'channel_group')