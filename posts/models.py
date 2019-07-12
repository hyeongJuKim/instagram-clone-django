from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings
from django.dispatch import receiver


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, help_text="최대 200자까지 입력 할 수 있습니다.")
    create_dt = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='upload/%Y/%M', blank=False)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-create_dt']


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
