from django.conf.urls import url
from posts.views import AddPostView, Posts, EditPost, DeletePost, MakePostNotRelevant, LikePost, WhoLiked, LikedPosts, \
    Profile, LeaveMessage

urlpatterns = [
                  url(r'^$', Posts.as_view(), name='posts'),
                  url(r'^add$', AddPostView.as_view(), name='add_post'),
                  url(r'^edit/(?P<post_id>[0-9]+)/$', EditPost.as_view(), name='edit_post'),
                  url(r'^save$', EditPost.as_view(), name='save_editions'),
                  url(r'^delete$', DeletePost.as_view(), name='delete_post'),
                  url(r'^make_not_relevant$', MakePostNotRelevant.as_view(), name='make_post_not_relevant'),
                  url(r'^like$', LikePost.as_view(), name='like_post'),
                  url(r'^leave_message$', LeaveMessage.as_view(), name='leave_message'),
                  url(r'^who_liked/(?P<post_id>[0-9]+)/$', WhoLiked.as_view(), name='who_liked'),
                  url(r'^liked/$', LikedPosts.as_view(), name='liked'),
                  url(r'^profile/$', Profile.as_view(), name='profile')
              ]
