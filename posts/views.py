from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.conf import settings
from django.http import JsonResponse
from models import Post
# User tests.
def anonimous_check(user):
    return  user.is_anonymous()

# Create your views here.
@user_passes_test(anonimous_check, login_url='/posts')
def index(request):
    """
        View for default page of unlogged user.
    """
    context = {
        'APP_ID': settings.VK_APP_ID,
        'GOOGLE_PLACES_API_KEY': settings.GOOGLE_PLACES_API_KEY,
    }
    return render(request, 'posts/auth.html', context)

@user_passes_test(anonimous_check, login_url='/posts')
def verify_hash(request):
    """
        Takes URL from vk.com redirect and tries to login user or create new user.
        Checks md5 checksum.
    """
    user = authenticate(uid=request.POST.get('uid'), hash=request.POST.get('hash'))
    if user is not None:
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.vkuser.photo_rec = request.POST.get('photo_rec')
        user.vkuser.place = request.POST.get('place')
        user.save()
        login(request, user)
        return JsonResponse({'success': 'true'})
    else:
        return JsonResponse({'fail': 'true'})

#post CRUD operations

@login_required
def add_post(request):
    if request.method == 'GET':
        return render(request, 'posts/add_post.html', {'has_active_post': request.user.vkuser.has_active_post})
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

@login_required
def posts(request):
    """
        View for default page of logged user.
    """
    context = {
        'posts_list': Post.objects.filter(place=request.user.vkuser.place, is_actual=True)
    }
    return render(request, 'posts/posts.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('../')
