from django.conf import settings
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)

def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)
class UploadImage(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='uploadImage')
    image = models.ImageField(upload_to=user_directory_path)

class Story(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='stories')
    title = models.TextField(blank=True, max_length=30)
    content = models.TextField(blank=True, max_length=2048)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def user_username(self):
        return self.user.username

    @property
    def user_profile_img(self):
        return self.user.profile_img

class Post(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, max_length=2048)
    created_date = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        'User', default=None, blank=True, related_name='like_posts')
    # image = models.ImageField(blank=True, upload_to='files/images/%Y/%m/%d/')

    @property
    def user_username(self):
        return self.user.username

    @property
    def user_profile_img(self):
        return self.user.profile_img


class Reply(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='replys')
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='replys')
    content = models.TextField(max_length=2048)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def user_username(self):
        return self.user.username

    @property
    def user_profile_img(self):
        return self.user.profile_img


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password,
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        db_index=True,
        max_length=255,
        unique=True,
    )

    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=False
    )

    google_id = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )

    profile_img = models.URLField(
        verbose_name="google's profile image url",
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
