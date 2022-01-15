import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, user_name, password=None):
        if not email:
            raise ValueError('이메일주소를 입력해주세요.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_name=user_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, user_name):
        user = self.create_user(
            email,
            password=password,
            name=name,
            user_name=user_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDERS = (
        ('M', '남성'),
        ('F', '여성'),
        ('N', '밝히고싶지 않음'),
    )

    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    name = models.CharField(verbose_name='name', max_length=20, blank=False)
    user_name = models.CharField(verbose_name='user_name', max_length=20, blank=False)
    comment = models.TextField(verbose_name='comment', max_length=255, blank=True)
    web_site = models.CharField(verbose_name='web_site', max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='upload/profile', blank=True)
    phone_number = models.CharField(verbose_name='phone_number', max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    search_fields = ['email']

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, help_text="최대 200자까지 입력 할 수 있습니다.")
    create_dt = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='upload/%Y/%M', blank=False)

    def __str__(self):
        return self.content

    def timesince_format(self):
        from django.utils.timesince import timesince
        return timesince(self.create_dt)

    class Meta:
        ordering = ['-create_dt']


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).profile_image
        new_file = instance.profile_image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except ValueError:
        return False
    except sender.DoesNotExist:
        return False
