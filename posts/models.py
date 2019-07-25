from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, user_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

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
        ('M', 'Male'),
        ('F', 'Female'),
    )

    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    name = models.CharField(verbose_name='name', max_length=20, blank=False)
    user_name = models.CharField(verbose_name='user_name', max_length=20, blank=False)
    comment = models.TextField(verbose_name='comment', max_length=255, blank=True)
    web_site = models.CharField(verbose_name='web_site', max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='upload/profile', blank=False)
    phone_number = models.CharField(verbose_name='phone_number', max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

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

    class Meta:
        ordering = ['-create_dt']


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
