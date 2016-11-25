from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.conf import settings
from django.http import JsonResponse
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
        'APP_ID': settings.VK_APP_ID
    }
    return render(request, 'posts/auth.html', context)

@user_passes_test(anonimous_check, login_url='/posts')
def verify_hash(request):
    """
        Takes URL from vk.com redirect and tries to login user or create new user.
        Checks md5 checksum.
    """
    #return JsonResponse({'success': request.POST.get('first_name')})

    user = authenticate(request.GET.get('uid'), request.GET.get('hash'))
    if user is not None:
        user.first_name = request.GET.get('first_name')
        user.last_name = request.GET.get('last_name')
        user.vkuser.photo_rec = request.GET.get('photo_rec')
        user.save()
        login(request, user)
        #return JsonResponse({'success': 'true'})
        return redirect('posts')
    else:
        #return JsonResponse({'success': 'false'})
        return redirect('index')

@login_required
def posts(request):
    """
        View for default page of logged user.
    """
    return render(request, 'posts/posts.html')

def logout_view(request):
    logout(request)
    return redirect('../')
