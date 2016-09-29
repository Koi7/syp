from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import hashlib
# Create your models here.
class VKUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_rec = models.CharField(max_length=200)
    has_active_post = models.BooleanField(default=False)
    last_point = models.CharField(max_length=100, default="")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        VKUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.vkuser.save()

class SearchPost(models.Model):
    content = models.CharField(max_length=500)
    pub_date = models.DateTimeFiled()


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
