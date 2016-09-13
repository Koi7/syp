from django.conf import settings
from django.contrib.auth.hashers import check_password
from posts.models import VK_User
import hashlib

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
