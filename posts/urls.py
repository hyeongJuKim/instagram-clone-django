from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.Posts.as_view(), name='posts'),
    path('users/profile/<int:pk>', views.User.as_view(), name='profile'),
    path('users/profile-page/', views.user_page, name='profile_page'),
    path('users/profile-update/<int:pk>', views.UserUpdate.as_view(), name='profile_update'),
    path('users/signup/', views.Signup.as_view(), name='signup'),
    path('users/forget-password/', views.password_reset_request, name='forget-password'),
    path('users/reset-password/', views.password_reset_response, name='reset-password'),
    path('users/', include('django.contrib.auth.urls')),
    path('posts/post-list/', views.Posts.as_view(), name='posts'),
    path('posts/posts-page/', views.posts_page, name='posts-page'),
    path('posts/<int:pk>', views.post, name='post'),
    path('posts/post-create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/post-update/<int:pk>', views.PostUpdate.as_view(), name='post-update'),
    path('posts/post-delete/<int:pk>', views.PostDelete.as_view(), name='post-delete'),
    path('ajax/validate-email/', views.validate_email, name='ajax-validate-eamil'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
django.contrib.auth.urls에 포함됨

accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
"""
