from django.conf.urls import url
from posts.views import AddPostView, Posts, DeletePost, LikePost, WhoLiked, LikedPosts, \
    Profile, LeaveMessage, MyPost, SaveProfileEditions, DeleteUser, PhotoUploader, PostsFilter, Notifications, CloseAttention

urlpatterns = [
                  url(r'^$', Posts.as_view(), name='posts'),
                  url(r'^add$', AddPostView.as_view(), name='add_post'),
                  url(r'^delete$', DeletePost.as_view(), name='delete_post'),
                  url(r'^like$', LikePost.as_view(), name='like_post'),
                  url(r'^leave_message$', LeaveMessage.as_view(), name='leave_message'),
                  url(r'^who_liked$', WhoLiked.as_view(), name='who_liked'),
                  url(r'^liked$', LikedPosts.as_view(), name='liked'),
                  url(r'^profile$', Profile.as_view(), name='profile'),
                  url(r'^my_posts$', MyPost.as_view(), name='my_posts'),
                  url(r'^save_profile_editions/$', SaveProfileEditions.as_view(), name='save_profile_editions'),
                  url(r'^delete_user$', DeleteUser.as_view(), name='delete_user'),
                  url(r'^upload_photo$', PhotoUploader.as_view(), name='upload_photo'),
                  url(r'^delete_photo(?:/(?P<qquuid>\S+))?', PhotoUploader.as_view(), name='delete_photo'),
                  url(r'^filter$', PostsFilter.as_view(), name='posts_filter'),
                  url(r'^notifications$', Notifications.as_view(), name='notifications'),
                  url(r'^close_attention$', CloseAttention.as_view(), name='close_attention'),
              ]
