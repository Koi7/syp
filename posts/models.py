# coding=utf-8
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, post_init
from django.contrib.auth.signals import user_logged_in
import hashlib
import json
import requests

# Create your models here.

# custom user one-to-one model
class VKUser(models.Model):
    # 0  is Sevast
    # 1  is Simf
    # 2  is Yalta
    PLACE_CHOICES = (
        (0, "Севастополь"),
        (1, "Симферополь"),
        (2, "Ялта"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_rec = models.CharField(max_length=200)
    has_active_post = models.BooleanField(default=False)
    place = models.IntegerField(choices=PLACE_CHOICES, default=1)
    age = models.IntegerField(default=0)
    about = models.CharField(max_length=4000, default="")
    @property
    def place_str(self):
        return self.get_place_display()

    @property
    def liked(self):
        likes = self.user.like_set.all()
        liked_posts_ids = []
        for like in likes:
            liked_posts_ids.append(like.post.id)
        return liked_posts_ids

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            VKUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.vkuser.save()

        # @receiver(user_logged_in, sender=User)
        # def update_user_profile(user, **kwargs):
        #     if not user.is_superuser:
        #         response = requests.get(settings.VK_API_URL, params={'v': '5.60',
        #                                                              'lang': settings.LANGUAGE_CODE[0:2],
        #                                                              'fields': 'photo_50,first_name,last_name',
        #                                                              'user_ids': user.username})
        #         for user_data in json.loads(response.text)['response']:
        #             user.vkuser.photo_rec = user_data['photo_50']
        #             user.first_name = user_data['first_name']
        #             user.last_name = user_data['last_name']
        #         user.vkuser.save()


def get_image_path(instance, filename):
    extension = instance.filename.split('.')[1]
    vk_uid = instance.user.username
    return os.path.join('photos', str(instance.user.username),
                        '{}.{}'.format(instance.id, extension))


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=2000)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=True)
    is_actual = models.BooleanField(default=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    hash_id = models.CharField(max_length=4000, default="")

    @property
    def likes(self):
        return self.like_set.all().count()

    @property
    def liked(self):
        return self.like_set.all()

    @property
    def tags(self):
        return self.posttag_set.all()

    def __unicode__(self):
        return u'{} {} {} {} {}'.format(self.id, self.text, self.pub_datetime, self.is_actual,
                                           self.is_anonymous)

class PostImage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, null=True)
    post = models.ForeignKey(Post, related_name='images', null=True)
    filename = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    message = models.CharField(max_length=500, default="")
    created = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    value = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return u'{}'.format(self.value)


class PostTag(models.Model):
    post = models.ForeignKey(Post)
    tag = models.ForeignKey(Tag)

# custom authentication backend
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
