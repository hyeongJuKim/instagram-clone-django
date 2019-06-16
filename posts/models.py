from django.db import models


class Post(models.Model):
    content = models.CharField(max_length=200, help_text="최대 200자까지 입력 할 수 있습니다.")
    create_dt = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_dt']
