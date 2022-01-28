import re

from django.db import models

# Create your models here.

from accounts.models import User
from Tags.models import Tag


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    content = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='timeline_photo/%Y/%m/%d')
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    like = models.ManyToManyField(User)
    tag_set = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        old_tags = self.tag_set.all()
        new_tags = self.extract_tag_list()

        delete_tags: list[Tag] = []
        add_tags: list[Tag] = []

        for old_tag in old_tags:
            if not old_tag in new_tags:
                delete_tags.append(old_tag)

        for new_tag in new_tags:
            if not new_tag in old_tags:
                add_tags.append(new_tag)

        for delete_tag in delete_tags:
            self.tag_set.remove(delete_tag)

        for add_tag in add_tags:
            self.tag_set.add(add_tag)

    def extract_tag_list(self) -> list[Tag, ...]:
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.content)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-reg_date']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.CASCADE)
