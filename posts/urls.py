from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^add_post', views.add_post, name='add_post'),
]