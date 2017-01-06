from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^add', views.add_post, name='add_post'),
    url(r'^edit/(?P<post_id>[0-9]+)/$', views.edit_post, name='edit_post'),
    url(r'^delete', views.delete_post, name='delete_post'),
]