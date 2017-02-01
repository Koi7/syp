# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.conf import settings
from django.http import JsonResponse
from models import Post, Like, Tag


def anonimous_check(user):
    return user.is_anonymous()


@user_passes_test(anonimous_check, login_url='/posts', redirect_field_name=None)
def index(request):
    """
        On GET:

        View for default page of unlogged user.

        On POST:

        Takes URL from vk.com redirect and tries to login user or create new user.
        Checks md5 checksum.

    """

    if request.method == 'GET':
        context = {
            'APP_ID': settings.VK_APP_ID,
            'GOOGLE_PLACES_API_KEY': settings.GOOGLE_PLACES_API_KEY,
        }
        return render(request, 'posts/auth.html', context)

    if request.method == 'POST':

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
                    'success': 'true',
                    'redirect': 'posts',
                })
            login(request, user)
            return json

        else:

            return JsonResponse({'fail': 'true'})


@user_passes_test(anonimous_check, login_url='/posts')
def verify_hash(request):
    """
        Takes URL from vk.com redirect and tries to login user or create new user.
        Checks md5 checksum.
    """
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
                'success': 'true',
                'redirect': 'posts',
            })
        login(request, user)
        return json
    else:
        return JsonResponse({'fail': 'true'})


@login_required(redirect_field_name=None)
def specify_place(request):

    """
        On GET:

        Returns page with form to specify place.

        On POST:

        User is redirected to this view when he's place field isn't specified.
        User's place field isn't specified only when he enters site first time.

    """

    if request.method == 'GET':
        context = {
            'GOOGLE_PLACES_API_KEY': settings.GOOGLE_PLACES_API_KEY,
        }
        return render(request, 'posts/specify_place.html', context)

    if request.method == 'POST':
        request.user.vkuser.place = request.POST.get('formatted_address')
        request.user.save()
        return JsonResponse({
            'success': request.POST.get('formatted_address'),
            'redirect': 'posts',
        })


# post CRUD operations

@login_required(redirect_field_name=None)
def add_post(request):

    """
        On GET:

        Returns page with form to add post.

        On POST:

        Tries to save new post.

    """

    if request.method == 'GET':
        context = {
            'has_active_post': request.user.vkuser.has_active_post,
            'tag_list': Tag.objects.all(),
        }
        return render(request, 'posts/add_post.html', context)

    if request.method == 'POST':
        if request.user.vkuser.has_active_post:
            actual_post = Post.objects.get(user=request.user, is_actual=True)
            actual_post.is_actual = False
            actual_post.save()
        post = Post()
        post.user = request.user
        post.text = request.POST.get('text')
        post.is_anonymous = True if request.POST.get('is_anonymous') == 'on' else False
        post.place = request.user.vkuser.place
        post.save()
        request.user.vkuser.has_active_post = True
        request.user.save()
        return redirect('posts')


@login_required(redirect_field_name=None)
def edit_post(request, post_id):

    if request.method == 'GET':
        post_to_edit = Post.objects.get(id=post_id)

        if request.user == post_to_edit.user:
            context = {
                'text': post_to_edit.text,
                'is_anonymous': post_to_edit.is_anonymous,
                'post_id': post_to_edit.id,
                'tag_list': Tag.objects.all(),
            }
            return render(request, 'posts/edit_post.html', context)


@login_required(redirect_field_name=None)
def save_editions(request):

    if request.method == 'POST':
        post_to_edit = Post.objects.get(id=request.POST.get('post_id'))
        if request.user == post_to_edit.user:
            post_to_edit.text = request.POST.get('text')
            post_to_edit.is_anonymous = True if request.POST.get('is_anonymous') == 'on' else False
            post_to_edit.save()
            return redirect('posts')


@login_required(redirect_field_name=None)
def delete_post(request):

    if request.method == 'POST':
        post_to_delete = Post.objects.get(id=get_post_id(request))
        if request.user == post_to_delete.user:
            if post_to_delete.is_actual:
                request.user.vkuser.has_active_post = False
                request.user.save()
            post_to_delete.delete()
    return redirect('posts')


@login_required(redirect_field_name=None)
def make_post_not_relevant(request):

    if request.method == 'POST':
        post = Post.objects.get(id=get_post_id(request))
        if request.user == post.user:
            post.is_actual = False
            request.user.vkuser.has_active_post = False
            post.save()
            request.user.save()
    return redirect('posts')


@login_required(redirect_field_name=None)
def like_post(request):

    if request.method == 'POST':
        like_obj, created = Like.objects.get_or_create(user=request.user, post_id=get_post_id(request))
        if created:
            like_obj.save()
        else:
            like_obj.delete()
    return redirect('posts')


@login_required(redirect_field_name=None)
def who_liked(request, post_id):

    if request.method == 'GET':
        post = Post.objects.get(id=post_id)
        context = {
            'post': post,
        }
        return render(request, 'posts/who_liked.html', context)


@login_required(redirect_field_name=None)
def liked(request):
    if request.method == 'GET':
        users_like_objects = Like.objects.filter(user=request.user)
        liked_posts_list = []
        for like in users_like_objects:
            liked_posts_list.append(Post.objects.get(id=like.post_id))
        context = {
            'liked_posts': liked_posts_list
        }
        return render(request, 'posts/liked.html', context)


def not_found(request):
    return HttpResponse('<div style="width: 400px; margin: 0 auto; text-align: center"><h1>НИХУЯ НЕТ</h2></div>')


@login_required(redirect_field_name=None)
def posts(request):

    """
        View for default page of logged user.
        Returns relevant posts list.
    """

    context = {
        'posts_list': Post.objects.filter(place=request.user.vkuser.place)
    }
    return render(request, 'posts/posts.html', context)


@login_required(redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect('../')


# utils
def get_post_id(request):
    return int(request.POST.get('post_id'))
