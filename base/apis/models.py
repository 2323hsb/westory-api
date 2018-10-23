from django.db import models
from django.utils import timezone

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField(blank=True, max_length=2048)
    created_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.created_date

# class Image(models.Model):
#     image = models.ImageField(blank=True, upload_to='files/images/%Y/%m/%d/')

class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
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
        max_length = 255,
        unique = True,
    )

    username = models.CharField(
        db_index=True, 
        max_length=255, 
        unique=False
    )

    google_id = models.CharField(
        db_index=True,
        max_length=255,
        unique=True
    )

    ''' 
        null = True: Record 생성 시 NULL값이 들어가는 것을 허용, Update시에는 불허함
        null = False: Record 생성 시 NULL값 비허용
        blank = True: Update 에서도 빈 값을 허용
    '''

    # profile = models.OneToOneField('profiles.Profile', on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# class OAuthUser(models.Model):
#     email = models.EmailField(
#         db_index = True,
#         max_length = 255,
#         unique = True,
#     )

#     name = models.CharField(
#         max_length=255, 
#         unique=False
#     )

#     auth_id = models.CharField(
#         max_length=255,
#         unique=True
#     )

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    