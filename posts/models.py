# coding=utf-8
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, post_init
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import hashlib
import json
import requests
import datetime
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
    SEX_CHOICES = (
        (-1, "не определено"),
        (0, "парень"),
        (1, "девушка"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_rec = models.CharField(max_length=200)
    has_active_post = models.BooleanField(default=False)
    place = models.IntegerField(choices=PLACE_CHOICES, default=1)
    age = models.IntegerField(default=0)
    sex = models.IntegerField(choices=SEX_CHOICES, default=-1)
    about = models.CharField(max_length=4000, default="")
    notifications_timestamp = models.DateTimeField(null=True)
    has_closed_attention = models.BooleanField(default=False)

    @property
    def sex_str(self):
        return self.get_sex_display()

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

    @property
    def unread_notifications_amount(self):
        return len(self.user.notification_set.filter(unread=True))


    @property
    def unread_notifications(self):
        return list(self.user.notification_set.filter(unread=True))

    @property
    def read_notifications(self):
        return list(self.user.notification_set.filter(unread=False))


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
    # 0  is Sevast
    # 1  is Simf
    # 2  is Yalta
    PLACE_CHOICES = (
        (-1, ""),
        (0, "Севастополь"),
        (1, "Симферополь"),
        (2, "Ялта"),
    )
    # 0  is Sevast
    # 1  is Simf
    # 2  is Yalta
    TAG_CHOICES = (
        (-1, ""),
        (0, "ищу парня"),
        (1, "ищу девушку"),
        (2, "ищу друга"),
        (3, "ищу подругу"),
        (4, "ищу компанию"),
        (5, "ищу с/о")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=2000)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=True)
    is_actual = models.BooleanField(default=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    place = models.IntegerField(choices=PLACE_CHOICES, default=-1)
    tag = models.IntegerField(choices=TAG_CHOICES, default=-1)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    @property
    def place_str(self):
        return self.get_place_display()
        
    @property
    def tag_str(self):
        return self.get_tag_display()

    @property
    def likes(self):
        return self.like_set.all().count()

    @property
    def liked(self):
        return self.like_set.all()

    @property
    def photos(self):
        return self.postimage_set.all()

    def __unicode__(self):
        return u'{} {} {} {} {}'.format(self.id, self.text, self.pub_datetime, self.is_actual,
                                           self.is_anonymous)

class PostImage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, null=True)
    post = models.ForeignKey(Post, null=True)
    filename = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    message = models.CharField(max_length=500, default="")
    created = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    VERB_CHOICES = (
        (-1, 'no'),
        (0, 'like'),
        (1, 'message'),
        (2, 'accepted'),
        (3, 'rejected')
    )
    user = models.ForeignKey(User)
    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor', null=True)
    actor_object_id = models.CharField(max_length=255, default="")
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')    
    verb = models.CharField(choices=VERB_CHOICES, default=-1, max_length=20)
    target = models.ForeignKey(Post)
    message = models.CharField(max_length=2000, default="")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    unread = models.BooleanField(default=True)
    
    @property
    def verb_str(self):
        return self.get_verb_display()

    @receiver(post_save, sender=Like)
    def notify_like(instance, created, **kwargs):
        """Create new notification if there a new like."""
        # If reciever is called on create method - return.
        # Create notification only if reciever is called on save method!!!
        if created:
            return
        new_notification = Notification()
        new_notification.user = instance.post.user
        new_notification.actor_content_type = ContentType.objects.get_for_model(instance.user)
        new_notification.actor_object_id = instance.user.id
        # 0 means LIKE verb
        if instance.message:
            new_notification.verb = 'message'
        else:
            new_notification.verb = 'like'
        new_notification.target = instance.post
        new_notification.save()

    @receiver(post_save, sender=Post)
    def notify_accepted(instance, created, **kwargs):
        if instance.accepted:
            new_notification = Notification(user=instance.user, verb=2, target=instance)
            new_notification.save()
        else:
            try:
                # try to delete notification
                notifications_to_delete = Notification.objects.filter(user=instance.user, target=instance, verb=2)
                for notification in notifications_to_delete:
                    notification.delete()
            except Notification.DoesNotExist:
                pass

    @receiver(post_save, sender=Post)
    def notify_rejected(instance, created, **kwargs):
        if instance.rejected:
            new_notification = Notification(user=instance.user, verb=3, target=instance)
            new_notification.save()
        else:
            try:
                # try to delete notification
                notifications_to_delete = Notification.objects.filter(user=instance.user, target=instance, verb=3)
                for notification in notifications_to_delete:
                    notification.delete()
            except Notification.DoesNotExist:
                pass


    @receiver(post_delete, sender=Post)
    def deleted_all_related_notifications_post(instance, **kwargs):
        """ Deletes any Notification object connected to Post object being deleted. """
        pass

    @receiver(post_delete, sender=Like)
    def deleted_all_related_notifications_like(instance, **kwargs):
        """ Deletes any Notification object connected to Like object being deleted. """
        try:
            notifications_to_delete = Notification.objects.filter(user=instance.post.user, target=instance.post)
            for notification in notifications_to_delete:
                notification.delete()
        except Notification.DoesNotExist:
            pass



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
