from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
import hashlib
import json
import requests

#Create your models here.

#custom user one-to-one model
class VKUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_rec = models.CharField(max_length=200)
    has_active_post = models.BooleanField(default=False)
    last_place = models.CharField(max_length=200, default="")
    place = models.CharField(max_length=200, default="")
    age = models.IntegerField(default=0)
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            VKUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.vkuser.save()

    @receiver(user_logged_in, sender=User)
    def update_user_profile(user, **kwargs):
        if not user.is_superuser:
            response = requests.get(settings.VK_API_URL, params={'v': '5.60',
                                                                 'lang': settings.LANGUAGE_CODE[0:2],
                                                                 'fields': 'photo_50,first_name,last_name',
                                                                 'user_ids': user.username})
            for user_data in json.loads(response.text)['response']:
                user.vkuser.photo_rec = user_data['photo_50']
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.vkuser.save()

# post model
class Post(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    place = models.CharField(max_length=200, default="")
    text = models.CharField(max_length=2000)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=True)
    is_actual = models.BooleanField(default=True)
    users_liked_ids = models.CharField(max_length=50)

#custom authentication backend
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
