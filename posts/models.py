from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
import hashlib
from django.conf import settings
# Create your models here.
class VKUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_rec = models.CharField(max_length=200)
    has_active_post = models.BooleanField(default=False)
    last_point = models.CharField(max_length=100, default="")
'''
@python_2_unicode_compatible
class VK_User(AbstractBaseUser):
    uid = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo_rec = models.CharField(max_length=200)
    has_active_post = models.BooleanField(default=False)
    last_point = models.CharField(max_length=100, default="")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    has_module_perms
    USERNAME_FIELD = 'uid'
    def __str__(self):
        return "%s %s %d" % (self.first_name, self.last_name, self.uid)
'''
class HashBackend(object):

    def authenticate(self, uid, hash):
        md5 = hashlib.md5()
        md5.update(settings.VK_APP_ID + uid + settings.VK_API_SECRET)
        if md5.hexdigest() == hash:
            try:
                vk_user = User.objects.get(username=uid)
            except User.DoesNotExist:
                vk_user = User(username=uid)
                vk_user.save()
            return vk_user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
