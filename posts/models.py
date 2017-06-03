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
from django.utils.html import mark_safe
from django.core.paginator import Paginator
import hashlib
import json
import requests
import datetime

# utils 

def get_image_path(instance, filename):
    extension = instance.filename.split('.')[1]
    vk_uid = instance.user.username
    return os.path.join('photos', str(instance.user.username),
                        '{}.{}'.format(instance.id, extension))

# Create your models here.

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    text = models.CharField('Текст', max_length=2000)
    pub_datetime = models.DateTimeField('Прислано', auto_now_add=True)
    accepted_datetime = models.DateTimeField('Одобрено', null=True)
    is_anonymous = models.BooleanField('Анонимный?', default=True)
    place = models.IntegerField('Место', choices=PLACE_CHOICES, default=-1)
    tag = models.IntegerField('Тэг', choices=TAG_CHOICES, default=-1)
    accepted = models.BooleanField('Одобрено', default=False)
    rejected = models.BooleanField('Отвергнуто', default=False)

    class Meta:
        ordering = ['-accepted_datetime']

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

    @property 
    def photos_tags(self):
        photos = self.postimage_set.all()
        image_tags = []
        if photos:
            for photo in photos:
                image_tags.append('<img src="{}" width="100" heigth="100">'.format(photo.image.url))
        return mark_safe("".join(image_tags))


    def __unicode__(self):
        return u'{} {} {} {}'.format(self.id, self.text, self.pub_datetime, self.is_anonymous)

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
    place = models.IntegerField(choices=PLACE_CHOICES, default=1)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    age = models.IntegerField(default=0)
    sex = models.IntegerField(choices=SEX_CHOICES, default=-1)
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
        (0, 'лайкну{} ваш акутальный пост.'),
        (1, 'остави{} послание к вашему актуальному посту.'),
        (2, 'Ваш пост опубликован.'),
        (3, 'Ваш пост нарушает правила сайта, поэтому он не будет опубликован.')
    )
    user = models.ForeignKey(User)
    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor', null=True)
    actor_object_id = models.CharField(max_length=255, default="")
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')    
    verb = models.IntegerField(choices=VERB_CHOICES, default=-1)
    target = models.ForeignKey(Post)
    message = models.CharField(max_length=2000, default="")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']
    
    @property
    def verb_str(self):
        if self.verb == 0 or self.verb == 1:
            if self.actor.vkuser.sex == 0:
                return self.get_verb_display().format('л')
            if self.actor.vkuser.sex == 1:
                return self.get_verb_display().format('ла')
            if self.actor.vkuser.sex == -1:
                return self.get_verb_display().format('л(-а)')
        else:
            return self.get_verb_display()

    @receiver(post_save, sender=Like)
    def notify_like_and_message(instance, created, **kwargs):
        """Create new notification if there a new like."""
        # If reciever is called on create method - return.
        # Create notification only if reciever is called on save method!!!
        if created:
            return
        new_notification = Notification(
            user=instance.post.author,
            actor_content_type=ContentType.objects.get_for_model(instance.user),
            actor_object_id=instance.user.id,
            target=instance.post
        )
        if instance.message:
            new_notification.verb = 1
        else:
            new_notification.verb = 0
        new_notification.save()

    @receiver(post_save, sender=Post)
    def notify_accepted(instance, created, **kwargs):
        if instance.accepted:
            new_notification = Notification(user=instance.author, verb=2, target=instance)
            new_notification.save()
        else:
            try:
                # try to delete notification
                notifications_to_delete = Notification.objects.filter(user=instance.author, target=instance, verb=2)
                for notification in notifications_to_delete:
                    notification.delete()
            except Notification.DoesNotExist:
                pass

    @receiver(post_save, sender=Post)
    def notify_rejected(instance, created, **kwargs):
        if instance.rejected:
            new_notification = Notification(user=instance.author, verb=3, target=instance, verb_long=reject_message)
            new_notification.save()
        else:
            try:
                # try to delete notification
                notifications_to_delete = Notification.objects.filter(user=instance.author, target=instance, verb=3)
                for notification in notifications_to_delete:
                    notification.delete()
            except Notification.DoesNotExist:
                pass


    @receiver(post_delete, sender=Post)
    def deleted_all_related_notifications_post(instance, **kwargs):
        """ Deletes any Notification object connected to Post object being deleted. """
        try:
            # try to delete notification
            notifications_to_delete = Notification.objects.filter(target=instance)
            for notification in notifications_to_delete:
                notification.delete()
        except Notification.DoesNotExist:
            pass

    @receiver(post_delete, sender=Like)
    def deleted_all_related_notifications_like(instance, **kwargs):
        """ Deletes any Notification object connected to Like object being deleted. """
        try:
            notifications_to_delete = Notification.objects.filter(user=instance.post.author, target=instance.post, verb=0) | Notification.objects.filter(user=instance.post.author, target=instance.post, verb=1)
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
