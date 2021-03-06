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
from django.db.models import Q
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
    brand_icon = models.ImageField('Логотип', upload_to=get_ad_image_path, blank=True, null=True)
    brand_ofsite = models.CharField('Сайт брэнда', max_length=150, default="")
    text = models.CharField('Текст', max_length=2000)
    place = models.IntegerField('Место', choices=PLACE_CHOICES, default=-1, db_index=True)
    pub_datetime = models.DateTimeField('Создано', auto_now_add=True)
    days = models.IntegerField('Срок (дней)', default=-1)
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
    
    @property
    def is_active(self):
        delta = self.pub_datetime + timedelta(days=self.days)
        today = timezone.now()
        diff = today - delta
        if diff.days < 0:
            return True
        else:
            return False
    @property
    def brand_ofsite_as_link(self):
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(self.brand_ofsite, self.brand))

    @property
    def brand_icon_as_image(self):
        return mark_safe('<img src="{}" width="100" heigth="100">'.format(self.brand_icon.url))

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор', db_index=True)
    text = models.CharField('Текст', max_length=2000)
    pub_datetime = models.DateTimeField('Прислано', auto_now_add=True)
    is_anonymous = models.BooleanField('Анонимный?', default=True, db_index=True)
    place = models.IntegerField('Место', choices=PLACE_CHOICES, default=-1, db_index=True)
    tag = models.IntegerField('Тэг', choices=TAG_CHOICES, default=-1, db_index=True)
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

@receiver(post_save, sender=Post)
def notify_new_post(instance, created, **kwargs):
    if created:
        from django.core.mail import send_mail
        try:
            send_mail("Новый пост", "Новый пост на сайте!", u"admin@ищутебякрым.рф", ["izmaylov.ramazan@yandex.ru"], fail_silently=False,)
        except:
            pass

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
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
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
    def notifications_amount(self):
        return len(self.user.notification_set.filter(unread=True))


    @property
    def notifications(self):
        return list(self.user.notification_set.all())

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

    @receiver(user_logged_in, sender=User)
    def update_user_profile(user, **kwargs):
        if not user.is_superuser and not settings.DEV:
            response = requests.get(settings.VK_API_URL, params={'v': '5.62', 'lang': settings.LANGUAGE_CODE[0:2], 'fields': 'sex,photo_100', 'user_ids': user.username})
            for user_data in json.loads(response.text)['response']:
                user.vkuser.sex = user_data['sex']
                user.vkuser.photo_rec = user_data['photo_100']
            user.vkuser.save()
    
    def mark_read(self):
        unread = self.user.notification_set.filter(unread=True)
        for notification in unread:
            notification.unread = False
            notification.save()

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
    user = models.ForeignKey(User, db_index=True)
    post = models.ForeignKey(Post, db_index=True)
    message = models.CharField(max_length=500, default="")
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']

class Notification(models.Model):
    VERB_CHOICES = (
        (-1, 'no'),
        (0, 'лайкну{} ваш <a href="{}посты/мой" class="w3-text-blue link-no-style classic-hover" title="Список людей, которым понравился пост.">пост</a>.'),
        (1, 'остави{} вам <a href="{}посты/понравилось?post_id={}" class="w3-text-blue link-no-style classic-hover" title="Список людей, которым понравился пост.">послание</a>.'),
        (2, 'Ваш <a href="{}посты/мой" class="w3-text-blue link-no-style classic-hover" title="Список людей, которым понравился пост.">пост</a> опубликован.'),
        (3, 'Ваш <a href="{}посты/мой" class="w3-text-blue link-no-style classic-hover" title="Список людей, которым понравился пост.">пост</a> нарушает правила сайта, поэтому он не будет опубликован.'),
    )
    user = models.ForeignKey(User, null=True, db_index=True)
    actor = models.ForeignKey(VKUser, null=True, db_index=True)  
    verb = models.IntegerField(choices=VERB_CHOICES, default=-1)
    target = models.ForeignKey(Post, db_index=True)
    like = models.ForeignKey(Like, null=True, db_index=True)
    message = models.CharField(max_length=2000, default="")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    unread = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
    
    @property
    def verb_str(self):
        if self.verb == 0:
            if self.actor.sex == 2:
                return mark_safe(self.get_verb_display().format('л', settings.ENV_BASE))
            if self.actor.sex == 1:
                return mark_safe(self.get_verb_display().format('ла', settings.ENV_BASE))
        if self.verb == 1:
            if self.actor.sex == 2:
                return mark_safe(self.get_verb_display().format('л', settings.ENV_BASE, self.target.id))
            if self.actor.sex == 1:
                return mark_safe(self.get_verb_display().format('ла', settings.ENV_BASE, self.target.id))
        return mark_safe(self.get_verb_display().format(settings.ENV_BASE))

    @receiver(post_save, sender=Like)
    def notify_like_and_message(instance, created, **kwargs):
        """Create new notification if there a new like."""
        # If reciever is called on create method - return.
        # Create notification only if reciever is called on save method!!!
        if created:         
            if not instance.message:
                # like if message is empty
                new_notification = Notification(
                    user=instance.post.author,
                    actor=instance.user.vkuser,
                    target=instance.post,
                    like=instance
                )
                new_notification.verb = 0
                new_notification.save()
                return
            else:
                # message otherwise
                new_notification = Notification(
                    user=instance.post.author,
                    actor=instance.user.vkuser,
                    target=instance.post,
                    like=instance
                )
                new_notification.verb = 1
                new_notification.save()
                return
        else:
            if instance.message:
                new_notification = Notification(
                    user=instance.post.author,
                    actor=instance.user.vkuser,
                    target=instance.post,
                    like=instance
                )
                new_notification.verb = 1
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
