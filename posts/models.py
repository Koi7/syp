from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
import hashlib

#Create your models here.

#custom user one-to-one model
class VKUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_rec = models.CharField(max_length=200)
    has_active_post = models.BooleanField(default=False)
    last_point = models.CharField(max_length=100, default="")
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
            vk_api_url = 'https://api.vk.com/method/'
            vk_api_method = 'users.get'
            vk_api_parameter_names = iter(['user_ids', 'fields', 'v'])
            vk_api_parameters = iter([user.username, 'photo_50,first_name,last_name,city', '5.60'])
            #vk_api_request_url = "https://api.vk.com/method/users.get?user_ids=" + user.username + "&fields=photo_50,first_name,last_name&v=5.60"
            vk_api_request_url = '%s%s?%s=%s&%s=%s&%s=%s' % (vk_api_url,
                                                             vk_api_method,
                                                             next(vk_api_parameter_names),
                                                             next(vk_api_parameters),
                                                             next(vk_api_parameter_names),
                                                             next(vk_api_parameters),
                                                             next(vk_api_parameter_names),
                                                             next(vk_api_parameters))
            import json
            import urllib2
            response = urllib2.urlopen(vk_api_request_url)
            data = json.loads(response.read())
            for user_data in data['response']:
                user.vkuser.photo_rec = user_data['photo_50']
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.vkuser.save()

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
