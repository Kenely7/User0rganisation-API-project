# from django.db import models
# from django.contrib.auth.models import AbstractUser
# # Create your models here.
# import uuid

# class User(AbstractUser):
#     first_name =models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email =models.CharField(max_length=50, unique=True
#     password = models.CharField(max_length=100)
#     phone = models.CharField(max_length= 20)
#     default_organization = models.ForeignKey('Organisation', related_name='default_users', null=True, blank=True, on_delete=models.SET_NULL)


#     REQUIRED_FIELDS=[]
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    organisations = models.ForeignKey('Organisation', related_name='default_users', null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)



    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone']

    def __str__(self):
        return self.email


class Organisation(models.Model):
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField('User', related_name='organisation')

    

    def __str__(self):
        return self.name