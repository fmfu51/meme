from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    last_name = None
    first_name = None
    deta_joined = None
    reg_date = models.DateTimeField('등록날짜')
    update_date = models.DateTimeField('수정날짜')
    name = models.CharField('이름', max_length=100)