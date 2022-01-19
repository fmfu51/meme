from django.db import models

# Create your models here.
from accounts.models import User


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-reg_date']
