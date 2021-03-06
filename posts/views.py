# coding=utf-8
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from models import Post, Like, PostImage, Ad, BlackList
from django.core.paginator import Paginator
from django.contrib.staticfiles.templatetags.staticfiles import static
from faker import Factory
import json
import hashlib

# UTILS

def not_found(request):
    return render(request, 'posts/not_found.html')

def filter(place='any', tag='any', order='desc', is_anonymous=-1):

    posts_list = []

    filters = {
        'accepted': True,
    }

    if not place == 'any':
        filters['place'] = place
    if not tag == 'any':
        filters['tag'] = tag
    if not is_anonymous == 'any':
        filters['is_anonymous'] = True if is_anonymous == '0' else False

    posts_list = Post.objects.filter(**filters).order_by('-pub_datetime' if order == 'desc' else 'pub_datetime')

    return posts_list

def anonimous_check(user):
    return user.is_anonymous()

def not_in_blacklist(user):
    is_banned = BlackList.objects.filter(vk_id=user.username).exists()
    if is_banned:
        return False
    return True

def in_blacklist(user):
    is_banned = BlackList.objects.filter(vk_id=user.username).exists()
    if is_banned:
        return True
    return False

def make_read(notifications):
    for notification in notifications:
        notification.unread = False
        notification.save()

# CLASS-BASED VIEWS

class IndexView(View):
    template_name = 'posts/auth.html'
    dev_template_name = 'posts/dev_auth.html'

    @method_decorator(user_passes_test(anonimous_check, login_url='posts', redirect_field_name=None))
    def get(self, request):
        if settings.DEV:
            context = {

            }
            return render(request, self.dev_template_name, context)
        else:
            from django.contrib.auth.models import User
            context = {
                'APP_ID': settings.VK_APP_ID,
                'GOOGLE_PLACES_API_KEY': settings.GOOGLE_PLACES_API_KEY,
                'users': User.objects.all(),
            }
            return render(request, self.template_name, context)

class LoginView(View):
    
    @method_decorator(user_passes_test(anonimous_check, login_url='posts', redirect_field_name=None))
    def post(self, request):
        if settings.DEV:
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
                    import random
                    user.vkuser.sex = random.randint(1, 2)
                    if user.vkuser.sex == 2:
                        user.vkuser.photo_rec = static('posts/images/male_placeholder.svg')
                    else:
                        user.vkuser.photo_rec = static('posts/images/female_placeholder.svg')
                    # Generate name according to given sex.
                    if user.vkuser.sex == 2:
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
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.vkuser.photo_rec = request.POST.get('photo_rec')
                if not user.vkuser.photo_rec:
                    user.vkuser.photo_rec = static('posts/images/male_placeholder.svg')
                user.save()
                login(request, user)
                return JsonResponse({'success': 'true'})
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
        if place:
            request.user.vkuser.place = int(place)
        request.user.save()
        return JsonResponse({
            'success': True,
            'place': request.user.vkuser.place_str
            })

class PhotoUploader(View):

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
        # erase image from HDD
        path = post_image_to_delete.image.path
        print path
        if os.path.isfile(path):
            os.remove(path)
        return JsonResponse({
            'success': True
            })

class AddPostView(View):
    template_name = 'posts/add_post.html'

    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        return render(request, 'posts/add_post.html')

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):

        # MAKE OTHER POST NOT ACTUAL AND DELETE IT

        if request.user.vkuser.post and not request.user.username == "251791530":
            request.user.vkuser.post.delete()
            request.user.vkuser.post = None

        # BUILD NEW POST INSTANCE

        post = Post(author=request.user,
                    text=request.POST.get('text'),
                    is_anonymous=True if request.POST.get('is_anonymous') == 'true' else False,
                    place=request.POST.get('place'),
                    tag=request.POST.get('tag')
        )
        post.save()

        # ASSIGN TO USER

        request.user.vkuser.post = post

        # IMAGE HANDLING

        if request.POST.get('photos_json_string'):
            uploaded_photos_info = json.loads(request.POST.get('photos_json_string'))
            post_photo_list = []
            for photo_info in uploaded_photos_info:
                post_photo_list.append(PostImage.objects.get(id=photo_info['uuid']))
            if post_photo_list:
                for post_photo in post_photo_list:
                    post_photo.post = post
                    post_photo.has_post = True
                    post_photo.save()
        # SAVE CHANGES 

        request.user.save()

        return JsonResponse({
            'success': True
            })


class DeletePost(View):

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        
        Post.objects.get(pk=request.POST.get('post_id')).delete()

        return JsonResponse({
            'success': True
            })

class LikePost(View):
    redirect_to = 'posts'

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        post = Post.objects.get(id=request.POST.get('post_id'))
        is_created = False
        self_like = False
        if not request.user == post.author:
            like_obj, created = Like.objects.get_or_create(user=request.user, post_id=post.id)
            if created:
                like_obj.save()
            else:
                like_obj.delete()
                is_created = 1 # disliked
        else:
            self_like = True
        return JsonResponse({
            'is_created': is_created,
            'likes_amount': post.likes,
            'self_like': self_like
            })

class LeaveMessage(View):
    redirect_to = 'posts'

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        post = Post.objects.get(id=request.POST.get('post_id'))
        self_like = False
        err_msg = ''  
        success = False
        if not request.user == post.author:
            like_obj, created = Like.objects.get_or_create(user=request.user, post_id=post.id)            
            if  not like_obj.message:
                like_obj.message = request.POST.get('message').strip()
                like_obj.save()
                success = True
            else:
                err_msg = "Уже отправляли послание к этому посту."
        else:
            self_like = True
            success = False
        return JsonResponse({
            'success': success,
            'likes_amount': post.likes,
            'err_msg': err_msg,
            'self_like': self_like 
            })

class WhoLiked(View):
    template_name = 'posts/who_liked.html'
    ajax_template_name = 'posts/includes/like_list.html'
    like_items_per_request = 25

    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        # get post
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        # get page number
        offset = 1 if not request.GET.get('offset') else request.GET.get('offset')
        # init paginator 
        like_list_paginator = Paginator(post.liked, self.like_items_per_request)
        # get page
        like_list_paginator_page = like_list_paginator.page(offset)
        # serve ajax or default request
        if offset > 1:
            # serve ajax            
            context = {
                'like_list': like_list_paginator_page,
                'VK_BASE_URL': settings.VK_BASE_URL,
                'request': request,
            }
            rendered_template = render_to_string(self.ajax_template_name, context)
            return JsonResponse({
                'rendered_template': rendered_template,
                'has_next':  like_list_paginator_page.has_next(),
                'next_page': like_list_paginator_page.next_page_number() if like_list_paginator_page.has_next() else 0,
            })
        else:
            # serve default request
            context = {
                'like_list': like_list_paginator_page,
                'has_next':  like_list_paginator_page.has_next(),
                'next_page': like_list_paginator_page.next_page_number() if like_list_paginator_page.has_next() else 0,
                'post_id': post_id,
                'VK_BASE_URL': settings.VK_BASE_URL,
            }
            return render(request, self.template_name, context)

class MyPost(View):
    template_name = 'posts/my_post.html'

    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        context = {
            'posts_list': Post.objects.filter(author=request.user),
            'VK_BASE_URL': settings.VK_BASE_URL,
        }
        return render(request, self.template_name, context)

class LikedPosts(View):
    template_name = 'posts/liked.html'
    ajax_template_name = 'posts/includes/post_card.html'
    posts_per_request = 25

    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        users_like_objects = Like.objects.filter(user=request.user)
        offset = 1 if not request.GET.get('offset') else request.GET.get('offset')

        # init paginator 

        liked_post_list_paginator = Paginator(request.user.vkuser.liked, self.posts_per_request)
        liked_post_list_paginator_page =  liked_post_list_paginator.page(offset)

        if offset == 1:
            context = {
                'posts_list': liked_post_list_paginator_page,
                'has_next': liked_post_list_paginator_page.has_next(),
                'next_page': liked_post_list_paginator_page.next_page_number() if liked_post_list_paginator_page.has_next() else 0,
                'VK_BASE_URL': settings.VK_BASE_URL,
            }
            return render(request, self.template_name, context)
        elif offset > 1:
            context = {
                'posts_list': liked_post_list_paginator_page,
                'request': request,
                'VK_BASE_URL': settings.VK_BASE_URL,
            }
            rendered_template = render_to_string(self.ajax_template_name, context)
            return JsonResponse({
                'success': True,
                'rendered_template': rendered_template,
                'has_next': liked_post_list_paginator_page.has_next(),
                'next_page': liked_post_list_paginator_page.next_page_number() if liked_post_list_paginator_page.has_next() else 0
            })

class Posts(View):
    template_name = 'posts/posts.html'
    ajax_post_list_template = 'posts/includes/post_list.html'
    no_results_template = 'posts/no_results_html'
    post_per_request = 25

    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):

        """
            View for default page of logged user.
            Returns relevant posts list.
        """
        # GET PARAMETERS 

        place = request.user.vkuser.place if not request.GET.get('place') else request.GET.get('place')
        tag = "any" if not request.GET.get('tag') else request.GET.get('tag')
        order = "desc" if not request.GET.get('order') else request.GET.get('order')
        is_anonymous = 'any' if not request.GET.get('is_anonymous') else request.GET.get('is_anonymous')

        # FILTER POSTS

        filtered_posts = filter(place, tag, order, is_anonymous)        
        # RESOLVE AD

        ad = None
        if Ad.objects.filter(place=-1).exists():
            ad = Ad.objects.filter(place=-1).first()
        elif Ad.objects.filter(place=request.user.vkuser.place).exists():
            ad = Ad.objects.filter(place=request.user.vkuser.place).first()
        # INIT PAGINATOR

        filtered_posts_paginator = Paginator(filtered_posts, self.post_per_request)

        # BUILD CONTEXT

        context = {}


        filtered_posts_page = filtered_posts_paginator.page(1)

        context = {
            'posts_list': filtered_posts_page,
            'has_next': filtered_posts_page.has_next(),
            'next_page': filtered_posts_page.next_page_number() if filtered_posts_page.has_next() else 0,
            'VK_BASE_URL': settings.VK_BASE_URL,
            'ad': ad
        }

        return render(request, self.template_name, context)

class PostsFilter(View):
    template_name = 'posts/includes/post_list.html'
    template_name_li = 'posts/includes/post_card.html'
    no_results_template = 'posts/includes/no_results.html'
    post_per_request = 25
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request, *args, **kwargs):

        # GET PARAMETERS

        place = request.user.vkuser.place if not request.GET.get('place') else request.GET.get('place')
        tag = "any" if not request.GET.get('tag') else request.GET.get('tag')
        order = "desc" if not request.GET.get('order') else request.GET.get('order')
        is_anonymous = 'any' if not request.GET.get('is_anonymous') else request.GET.get('is_anonymous')
        offset = 1 if not request.GET.get('offset') else request.GET.get('offset')

        # FILTER POSTS 

        filtered_posts = filter(place, tag, order, is_anonymous)

        # INIT PAGINATOR 

        filtered_posts_paginator = Paginator(filtered_posts, self.post_per_request)

        # GET PAGE

        filtered_posts_page = filtered_posts_paginator.page(offset)


        # RENDER
        rendered_template = ''
        context = {}
        if offset == 1:
            # render ul and li and load more
            if filtered_posts_page:
                context = {
                    'posts_list': filtered_posts_page,
                    'has_next': filtered_posts_page.has_next(),
                    'next_page': filtered_posts_page.next_page_number() if filtered_posts_page.has_next() else 0,
                    'request': request,
                    'VK_BASE_URL': settings.VK_BASE_URL,
                }
                rendered_template = render_to_string(self.template_name, context)
            else:
                context = {
                    'message': 'Ничего не нашлось.',
                }
                rendered_template = render_to_string(self.no_results_template, context)
            return JsonResponse({
                'success': True,
                'rendered_template': rendered_template,
            })
        elif offset > 1:
            context = {
                'posts_list': filtered_posts_page,
                'request': request,
                'VK_BASE_URL': settings.VK_BASE_URL,
            }
            rendered_template = render_to_string(self.template_name_li, context)
            return JsonResponse({
                'success': True,
                'rendered_template': rendered_template,
                'has_next': filtered_posts_page.has_next(),
                'next_page': filtered_posts_page.next_page_number() if filtered_posts_page.has_next() else 0,
            })

class Notifications(View):
    template_name = 'posts/notifications.html'
    render_template_name = 'posts/includes/notifications_list.html'
    notifications_per_request = 25
    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):

        # make viwed notifications read

        # load data       

        notifications = request.user.vkuser.notifications
        context = {}

        # init paginators
        paginator = Paginator(notifications, self.notifications_per_request)
        # build context

        page = paginator.page(1)
        context = {
            'notifications_list': page,
            'has_next': page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else 0,
            'VK_BASE_URL': settings.VK_BASE_URL,
        }   

        # mark all unread notifications as read 
        request.user.vkuser.mark_read()      
        return render(request, self.template_name, context)


        



class NotificationsAjax(View):

    render_template_name = 'posts/includes/notifications_list.html'
    notifications_per_request = 25
    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        offset = request.GET.get('offset')
        # ajax
        if offset > 1:
            notifications = request.user.vkuser.notifications
            paginator = Paginator(notifications, self.notifications_per_request)
            page = paginator.page(offset)

            context = {
                'notifications_list': page,
                'VK_BASE_URL': settings.VK_BASE_URL,
            }

            rendered_template = render_to_string(self.render_template_name, context)
            return JsonResponse({
                'success': True,
                'rendered_template': rendered_template,
                'has_next': page.has_next(),
                'next_page': page.next_page_number() if page.has_next() else 0,
                'VK_BASE_URL': settings.VK_BASE_URL,
            })


 



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

    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        return render(request, self.template_name)
class About(View):
    template_name = 'posts/about.html'

    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        return render(request, self.template_name)

class Contacts(View):
    template_name = 'posts/contacts.html'

    @method_decorator(user_passes_test(not_in_blacklist, login_url='ban', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        return render(request, self.template_name)

class Ban(View):
    template_name = 'posts/ban.html'
    @method_decorator(user_passes_test(in_blacklist, login_url='/', redirect_field_name=None))
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        logout(request)
        return render(request, self.template_name)


@login_required(redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect('../')


