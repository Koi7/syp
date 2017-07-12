# coding=utf-8
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.signals import user_logged_in
from django.utils.html import mark_safe
from PIL import Image as Img, ExifTags
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import timedelta
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose
from django.core.exceptions import ObjectDoesNotExist
import StringIO
import hashlib
import json
import requests
import shutil
import uuid
# utils 

def get_image_path(instance, filename):
    extension = instance.filename.split('.')[1]
    return os.path.join('photos', str(instance.user.username),
                        '{}.{}'.format(instance.id, extension))

def get_ad_image_path(instance, filename):
    return os.path.join('ad_photos', instance.brand , '{}.{}'.format(uuid.uuid4().hex, 'jpg'))
# Create your models here.

class Ad(models.Model):
    PLACE_CHOICES = (
        (-1, "Все"),
        (0, "Севастополь"),
        (1, "Симферополь"),
        (2, "Ялта"),
    )

    image_width = 500
    image_height = 500
    quality = 70

    brand = models.CharField('Брэнд', max_length=50)
    brand_icon = models.ImageField(upload_to=get_ad_image_path, blank=True, null=True)
    text = models.CharField('Текст', max_length=2000)
    place = models.IntegerField('Место', choices=PLACE_CHOICES, default=-1)
    pub_datetime = models.DateTimeField('Создано', auto_now_add=True)
    accepted = models.BooleanField('Одобрено', default=False)
    image1 = ProcessedImageField(upload_to=get_ad_image_path,
                                        processors=[ResizeToFit(image_width, image_height)],
                                        format='JPEG',
                                        options={'quality': quality},
                                        blank=True,
                                        null=True)
    image2 = ProcessedImageField(upload_to=get_ad_image_path,
                                        processors=[ResizeToFit(image_width, image_height)],
                                        format='JPEG',
                                        options={'quality': quality},
                                        blank=True,
                                        null=True)
    image3 = ProcessedImageField(upload_to=get_ad_image_path,
                                        processors=[ResizeToFit(image_width, image_height)],
                                        format='JPEG',
                                        options={'quality': quality},
                                        blank=True,
                                        null=True)
    image4 = ProcessedImageField(upload_to=get_ad_image_path,
                                        processors=[ResizeToFit(image_width, image_height)],
                                        format='JPEG',
                                        options={'quality': quality},
                                        blank=True,
                                        null=True)
    image5 = ProcessedImageField(upload_to=get_ad_image_path,
                                        processors=[ResizeToFit(image_width, image_height)],
                                        format='JPEG',
                                        options={'quality': quality},
                                        blank=True,
                                        null=True)
    image6 = ProcessedImageField(upload_to=get_ad_image_path,
                                        processors=[ResizeToFit(image_width, image_height)],
                                        format='JPEG',
                                        options={'quality': quality},
                                        blank=True,
                                        null=True)
    class Meta:
        verbose_name = 'Рекламу'
        verbose_name_plural = 'Реклама'
    
    def save(self, *args, **kwargs):
        for image in self.images_callable():
            if image:
                img = Img.open(StringIO.StringIO(image.read()))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((500, 500), Img.ANTIALIAS)
                output = StringIO.StringIO()
                img.save(output, format='JPEG', quality=70)
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation]=='Orientation':
                            break
                    exif=dict(img._getexif().items())
                    # fix orientation
                    if exif[orientation] == 3:
                        img=img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img=img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img=img.rotate(90, expand=True)
                    # determine basic orientation (landscape | portrait)
                    if exif[orientation] == 6 or exif[orientation] == 8:
                        self.is_portrait = True
                except AttributeError:
                    pass
                output.seek(0)
                img.save(output, format='JPEG', quality=70)
                image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', output.len, None)
        super(Ad, self).save(*args, **kwargs)    

    @property
    def images(self):
        images = []
        if self.image1:
            images.append(self.image1)
        if self.image2:
            images.append(self.image2)
        if self.image3:
            images.append(self.image3)
        if self.image4:
            images.append(self.image4)
        if self.image5:
            images.append(self.image5)
        if self.image6:
            images.append(self.image6)
        
        return images
    
    def images_callable(self):
        images = []
        if self.image1:
            images.append(self.image1)
        if self.image2:
            images.append(self.image2)
        if self.image3:
            images.append(self.image3)
        if self.image4:
            images.append(self.image4)
        if self.image5:
            images.append(self.image5)
        if self.image6:
            images.append(self.image6)
        return images

    @property
    def images_as_tags(self):
        image_tags = []
        for image in self.images:
            if image:
                image_tags.append('<img src="{}" width="100" heigth="100">'.format(image.url))
        return mark_safe("".join(image_tags))


# erase image on instance delete
@receiver(post_delete, sender=Ad)
def erase_ad_images(instance, **kwargs):
    for image in instance.images:
        if os.path.isfile(image.path):
            os.remove(image.path)


class BlackList(models.Model):
    vk_id = models.CharField('VK_ID', max_length=20, default="")
    reason = models.CharField('Причина', max_length=250, default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    days = models.IntegerField('Срок', default=-1)

    class Meta:
        verbose_name_plural = 'Черный список'

    @property
    def is_active(self):
        delta = self.timestamp + timedelta(days=self.days)
        today = timezone.now()
        diff = today - delta
        if diff.days < 0:
            return True
        else:
            return False


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
    TAG_CHOICES = (
        (-1, ""),
        (0, "ищу парня"),
        (1, "ищу девушку"),
        (2, "ищу друга"),
        (3, "ищу подругу"),
        (4, "ищу компанию"),
        (5, "ищу с/о"),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    text = models.CharField('Текст', max_length=2000)
    pub_datetime = models.DateTimeField('Прислано', auto_now_add=True)
    is_anonymous = models.BooleanField('Анонимный?', default=True)
    place = models.IntegerField('Место', choices=PLACE_CHOICES, default=-1)
    tag = models.IntegerField('Тэг', choices=TAG_CHOICES, default=-1)
    accepted = models.BooleanField('Одобрено', default=False)
    rejected = models.BooleanField('Отвергнуто', default=False)

    class Meta:
        verbose_name_plural = 'Посты'
        ordering = ['-pub_datetime']

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
        (2, "парень"),
        (1, "девушка"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_rec = models.CharField(max_length=200)
    place = models.IntegerField('Город', choices=PLACE_CHOICES, default=0)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    age = models.IntegerField('Возраст', default=0)
    sex = models.IntegerField('Пол', choices=SEX_CHOICES, default=-1)
    has_closed_attention = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Пользователи'


    @property
    def sex_str(self):
        return self.get_sex_display()

    @property
    def place_str(self):
        return self.get_place_display()

    @property
    def liked(self):
        likes = self.user.like_set.all()
        liked_posts = []
        for like in likes:
            liked_posts.append(like.post)
        return liked_posts

    @property
    def unread_notifications_amount(self):
        return len(self.user.notification_set.filter(unread=True))


    @property
    def unread_notifications(self):
        return list(self.user.notification_set.filter(unread=True))

    @property
    def read_notifications(self):
        return list(self.user.notification_set.filter(unread=False))

    @property
    def mark_read_notifications(self):
        return list(self.user.notification_set.filter(mark_read=True))

    @property 
    def photo(self):
        return mark_safe("".join('<img src="{}" width="100" heigth="100">'.format(self.photo_rec)))


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            VKUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.vkuser.save()

class PostImage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, null=True)
    post = models.ForeignKey(Post, null=True)
    filename = models.CharField(max_length=255, null=True)
    image = ProcessedImageField(upload_to=get_image_path,
                                processors=[Transpose(), ResizeToFit(500, 500)],
                                format='JPEG',
                                options={'quality': 70},
                                blank=True,
                                null=True)
    is_portrait = models.BooleanField(default=False)
    has_post =  models.BooleanField('Прикреплено', default=False)
    
    class Meta:
        verbose_name_plural = 'Фотографии'

    @property 
    def image_tag(self):
        return mark_safe("".join('<img src="{}" width="100" heigth="100">'.format(self.image.url)))
    

# erase image on instance delete
@receiver(post_delete, sender=PostImage)
def erase_images(instance, **kwargs):
    path = instance.image.path
    if os.path.isfile(path):
        os.remove(path)

    
class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    message = models.CharField(max_length=500, default="")
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']

class Notification(models.Model):
    VERB_CHOICES = (
        (-1, 'no'),
        (0, 'лайкну{} ваш пост.'),
        (2, 'Ваш пост опубликован.'),
        (3, 'Ваш пост нарушает правила сайта, поэтому он не будет опубликован.')
    )
    user = models.ForeignKey(User)
    actor = models.ForeignKey(VKUser, null=True)  
    verb = models.IntegerField(choices=VERB_CHOICES, default=-1)
    target = models.ForeignKey(Post)
    message = models.CharField(max_length=2000, default="")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']
    
    @property
    def verb_str(self):
        if self.verb == 0:
            if self.actor.sex == 2:
                return self.get_verb_display().format('л')
            if self.actor.sex == 1:
                return self.get_verb_display().format('ла')
        else:
            return self.get_verb_display()

    @receiver(post_save, sender=Like)
    def notify_like_and_message(instance, created, **kwargs):
        """Create new notification if there a new like."""
        # If reciever is called on create method - return.
        # Create notification only if reciever is called on save method!!!
        if created:
            new_notification = Notification(
                user=instance.post.author,
                actor=instance.user.vkuser,
                target=instance.post
            )
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
            new_notification = Notification(user=instance.author, verb=3, target=instance)
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
            notifications_to_delete = Notification.objects.filter(user=instance.post.author, actor=instance.user.vkuser, target=instance.post, verb=0)
            for notification in notifications_to_delete:
                notification.delete()
        except Notification.DoesNotExist:
            pass
        except ObjectDoesNotExist:
            notifications_to_delete = Notification.objects.filter(user=instance.post.author, target=instance.post, verb=0)
            for notification in notifications_to_delete:
                notification.delete()

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
