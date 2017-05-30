# coding=utf-8
# -*- coding: utf-8 -*-
import os

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.conf import settings
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views import View
from operator import attrgetter
from models import Post, Like, PostImage
from faker import Factory
from django.utils import timezone
from django.core.paginator import Paginator
import hashlib
import re
import json

# UTILS

def delete_image(path):
    if os.path.isfile(path):
        os.remove(path)

def not_found(request):
    return HttpResponse('<div style="width: 400px; margin: 0 auto; text-align: center"><h1>НИХУЯ НЕТ</h2></div>')



def anonimous_check(user):
    return user.is_anonymous()

# CLASS-BASED VIEWS

class IndexView(View):
    template_name = 'posts/auth.html'

    # @method_decorator(user_passes_test(anonimous_check, login_url='/posts', redirect_field_name=None))
    def get(self, request):
        if settings.LOCAL_DEV:
            context = {

            }
            return render(request, self.template_name, context)
        else:
            from django.contrib.auth.models import User
            context = {
                'APP_ID': settings.VK_APP_ID,
                'GOOGLE_PLACES_API_KEY': settings.GOOGLE_PLACES_API_KEY,
                'users': User.objects.all(),
            }
            return render(request, self.template_name, context)

    # @method_decorator(user_passes_test(anonimous_check, login_url='/posts', redirect_field_name=None))
    def post(self, request):
        if settings.LOCAL_DEV:
            need_new_user = True if request.POST.get('new') == 'on' else False
            if need_new_user:
                fake = Factory.create('ru_RU')
                uid = str(fake.random_number(9))
                md5 = hashlib.md5()
                md5.update(settings.VK_APP_ID + uid + settings.VK_API_SECRET)
                hash = md5.hexdigest()
                user = authenticate(uid=uid, hash=hash)
                if user is not None:
                    user.vkuser.place = int(request.POST.get('place'))
                    user.vkuser.photo_rec = ''
                    import random
                    user.vkuser.sex = random.randint(0, 1)
                    # Generate name according to given sex.
                    if user.vkuser.sex == 0:
                        user.first_name = fake.first_name_male()
                        user.last_name = fake.last_name_male()
                    else:
                        user.first_name = fake.first_name_female()
                        user.last_name = fake.last_name_female()
                    user.save()
                    login(request, user)
                    return redirect('posts')
                else:
                    return redirect('not_found')
            else:
                md5 = hashlib.md5()
                md5.update(settings.VK_APP_ID + request.POST.get('uid') + settings.VK_API_SECRET)
                hash = md5.hexdigest()
                user = authenticate(uid=request.POST.get('uid'), hash=hash)
                login(request, user)
                return redirect('posts')
        else:
            user = authenticate(uid=request.POST.get('uid'), hash=request.POST.get('hash'))
            if user is not None:
                if user.vkuser.place == "":
                    user.first_name = request.POST.get('first_name')
                    user.last_name = request.POST.get('last_name')
                    user.vkuser.photo_rec = request.POST.get('photo_rec')
                    user.save()
                    json = JsonResponse({
                        'success': 'true',
                        'redirect': 'specify_place',
                    })
                else:
                    json = JsonResponse({
                        'success': True,
                        'redirect': 'posts',
                    })
                login(request, user)
                return json
            else:
                return JsonResponse({'fail': 'true'})

class DeleteUser(View):

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        request.user.delete()
        logout(request)
        return JsonResponse({
            'success': True,
            })

class SaveProfileEditions(View):

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        place = request.POST.get('place')
        age = request.POST.get('age')
        about = request.POST.get('about')
        if place:
            request.user.vkuser.place = int(place)
        if age:
            request.user.vkuser.age = age
        if about:
            request.user,vkuser.about = about
        request.user.save()
        return JsonResponse({
            'success': True,
            'place': request.user.vkuser.place_str,
            'age': request.user.vkuser.age,
            'about': request.user.vkuser.about,
            })

class  PhotoUploader(View):

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        uuid = request.POST.get('qquuid')
        filename = request.POST.get('qqfilename')
        photo = PostImage(id=uuid, filename=filename, image=request.FILES['qqfile'], user=request.user)
        photo.save()
        return JsonResponse({
            'success': True
            })

    @method_decorator(login_required(redirect_field_name=None))
    def delete(self, request, qquuid):
        try:
            post_image_to_delete = PostImage.objects.get(id=qquuid)
        except Exception:
            return JsonResponse({
                'success': True
                })
        delete_image(post_image_to_delete.image.path)
        return JsonResponse({
            'success': True
            })

class AddPostView(View):
    template_name = 'posts/add_post.html'
    redirect_to = 'posts'
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        context = {
            'has_active_post': request.user.vkuser.has_active_post,
        }
        return render(request, 'posts/add_post.html', context)

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        # MAKE OTHER POST NOT ACTUAL
        if request.user.vkuser.has_active_post:
            actual_post = Post.objects.get(user=request.user, is_actual=True)
            actual_post.is_actual = False
            actual_post.save()
        # BUILD NEW POST INSTANCE
        post = Post()
        post.user = request.user
        post.text = request.POST.get('text')
        post.is_anonymous = True if request.POST.get('is_anonymous') == 'on' else False
        post.place = request.POST.get('place')
        post.tag = request.POST.get('tag')
        post.save()
        # add tag
        # IMAGE HANDLING
        if request.POST.get('photos_json_string'):
            uploaded_photos_info = json.loads(request.POST.get('photos_json_string'))
            post_photo_list = []
            for photo_info in uploaded_photos_info:
                post_photo_list.append(PostImage.objects.get(id=photo_info['uuid']))
            if post_photo_list:
                for post_photo in post_photo_list:
                    post_photo.post = post
                    post_photo.save()       
        request.user.vkuser.has_active_post = True
        request.user.save()
        return JsonResponse({
            'success': True
            })

    def is_clear(self, text):
        for word in self.words_to_filter:
            if bool(re.search(word, text)):
                return False
        return True


class EditPost(View):
    template_name = 'posts/edit_post.html'

    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request, post_id):
        post_to_edit = Post.objects.get(id=post_id)
        if request.user == post_to_edit.user:
            context = {
                'text': post_to_edit.text,
                'is_anonymous': post_to_edit.is_anonymous,
                'post_id': post_to_edit.id,
                'tag_list': Tag.objects.all(),
            }
            return render(request, 'posts/edit_post.html', context)

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        post_to_edit = Post.objects.get(id=request.POST.get('post_id'))
        if request.user == post_to_edit.user:
            post_to_edit.text = request.POST.get('text')
            post_to_edit.is_anonymous = True if request.POST.get('is_anonymous') == 'on' else False
            for tag_value in request.POST.getlist('tags'):
                post_tag = PostTag()
                post_tag.post = post_to_edit
                post_tag.tag = Tag.objects.get(value=tag_value)
                post_tag.save()
            if request.FILES['photo']:
                delete_image(post_to_edit.image.path)
                post_to_edit.image = request.FILES['photo']
            post_to_edit.save()
            return redirect('posts')


class DeletePost(View):
    redirect_to = 'posts'

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        post_to_delete = Post.objects.get(id=request.POST.get('post_id'))
        success = False
        if request.user == post_to_delete.user:
            if post_to_delete.is_actual:
                request.user.vkuser.has_active_post = False
                request.user.save()
            post_to_delete.delete()
            success = True
        return JsonResponse({
            'success': success
            })


class MakePostNotRelevant(View):
    redirect_to = 'posts'

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        post = Post.objects.get(id=request.POST.get('post_id'))
        success = False
        if request.user == post.user:
            post.is_actual = False
            request.user.vkuser.has_active_post = False
            post.save()
            request.user.save()
            success = True
        return JsonResponse({
            'success': success
        })


class LikePost(View):
    redirect_to = 'posts'
    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        post = Post.objects.get(id=request.POST.get('post_id'))
        like_obj, created = Like.objects.get_or_create(user=request.user, post_id=post.id)
        is_created = 0 # new like added
        if created:
            like_obj.save()
        else:
            like_obj.delete()
            is_created = 1 # disliked
        return JsonResponse({
            'is_created': is_created,
            'likes_amount': post.likes
            })

class LeaveMessage(View):
    redirect_to = 'posts'

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        post = Post.objects.get(id=request.POST.get('post_id'))
        like_obj, created = Like.objects.get_or_create(user=request.user, post_id=post.id)
        success = False
        err_msg = ''
        if  not like_obj.message:
            like_obj.message = request.POST.get('message').strip()
            like_obj.save()
            success = True
        else:
            err_msg = "Уже отправляли послание к этому посту."
        return JsonResponse({
            'success': success,
            'likes_amount': post.likes,
            'err_msg': err_msg
            })

class WhoLiked(View):
    template_name = 'posts/who_liked.html'

    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        context = {
            'post': post,
        }
        return render(request, self.template_name, context)


class MyPosts(View):
    template_name = 'posts/my_posts.html'

    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        user_posts = Post.objects.filter(user=request.user, rejected=False)
        context = {
            'user_posts_list': user_posts,
        }
        return render(request, self.template_name, context)

class LikedPosts(View):
    template_name = 'posts/liked.html'

    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        users_like_objects = Like.objects.filter(user=request.user)
        liked_posts_list = []
        for like in users_like_objects:
            liked_posts_list.append(Post.objects.get(id=like.post_id))
        context = {
            'liked_posts': liked_posts_list
        }
        return render(request, self.template_name, context)


class Posts(View):
    template_name = 'posts/posts.html'

    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        """
            View for default page of logged user.
            Returns relevant posts list.
        """
        post_list_by_place = list(Post.objects.filter(is_actual=True, accepted=True, place=request.user.vkuser.place))
        post_list_by_place.sort(key=attrgetter('pub_datetime'), reverse=True)
        context = {
            'posts_list': post_list_by_place,
        }
        return render(request, self.template_name, context)

class PostsFilter(View):
    template_name = 'posts/filtered_posts.html'

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        tag = request.POST.get('tag')
        place = int(request.POST.get('place'))
        order = request.POST.get('order')
        anonymous = int(request.POST.get('anonymous'))
        posts_list = []
        if tag == "any" and place == -1:
            posts_list = list(Post.objects.filter(is_actual=True, accepted=True))
        elif tag == "any" and place != -1:
            posts_list = list(Post.objects.filter(is_actual=True, place=place, accepted=True))
        elif tag != "any" and place == -1:
            posts_list = list(Post.objects.filter(is_actual=True, tag=tag, accepted=True))
        elif tag != "any" and place != -1:
            posts_list = list(Post.objects.filter(is_actual=True, place=place, tag=tag, accepted=True))
        # filter by anonymous
        if anonymous == 0:
            posts_list =  [obj for obj in posts_list if obj.is_anonymous == True]
        elif anonymous == 1:
            posts_list =  [obj for obj in posts_list if obj.is_anonymous == False]
        # order by date
        if order == 'acs':
            posts_list.sort(key=attrgetter('pub_datetime'), reverse=True)
        else:
            posts_list.sort(key=attrgetter('pub_datetime'))

        rendered_template = render_to_string(self.template_name, {'posts_list': posts_list, 'request':request})
        return JsonResponse({
            'success': True,
            'rendered_template': rendered_template
            })

class Notifications(View):
    template_name = 'posts/notifications.html'
    notifications_per_request = 5
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request, offset=None):
        # load data       

        read_notifications = request.user.vkuser.read_notifications
        unread_notifications = request.user.vkuser.unread_notifications
        context = {}

        # init paginators

        read_paginator = Paginator(read_notifications, self.notifications_per_request)

        # build context

        # not ajax
        if not offset:
            page_read = read_paginator.page(1)

            context = {
                'read_notifications': page_read,
                'unread_notifications': unread_notifications,
                'next_read': page_read.has_next(),
            }

            self.mark_read(context['unread_notifications'])

            return render(request, self.template_name, context)

        # ajax
        if offset and offset > 1:

            page_read = unread_paginator.page(offset)

            context = {
                'read_notifications': unread_paginator.page(offset),
                'has_next': page_read.has_next()
            }

            rendered_template = render_to_string(self.template_name, context)

            return JsonResponse({
                'success': True,
                'rendered_template': rendered_template
                })

    
        

    def mark_read(self, unread_notifications):
        for notification in unread_notifications:
            notification.unread = False
            notification.save()


class CloseAttention(View):

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        request.user.vkuser.has_closed_attention = True
        request.user.save()
        return JsonResponse({
            'success': True
            })

class Profile(View):
    template_name = 'posts/profile.html'

    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        return render(request, self.template_name)


@login_required(redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect('../')


