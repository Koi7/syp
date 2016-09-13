from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.encoding import python_2_unicode_compatible
import hashlib
from django.conf import settings
# Create your models here.
@python_2_unicode_compatible
class VK_User(AbstractBaseUser):
    uid = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo_rec_url = models.CharField(max_length=200)
    have_active_post = models.BooleanField(default=False)
    last_point = models.CharField(max_length=100, default="")
    USERNAME_FIELD = 'uid'
    def __str__(self):
        return "%s %s %d" % (self.first_name, self.last_name, self.uid)

class HashBackend(object):

    def authenticate(self, first_name=None, last_name=None, photo_rec=None, uid=None, hash=None):
        md5 = hashlib.md5()
        md5.update(settings.VK_APP_ID + uid + settings.VK_API_SECRET)
        if md5.digest() == hash:
            try:
                vk_user = VK_User.objects.get(uid=uid)
            except VK_User.DoesNotExist:
                vk_user = VK_User(uid=uid, first_name=first_name, last_name=last_name, photo_rec=photo_rec)
                vk_user.save()
            return vk_user
        return None

    def get_user(self, user_id):
        try:
            return VK_User.objects.get(pk=uid)
        except VK_User.DoesNotExist:
            return None
