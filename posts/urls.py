from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.Posts.as_view(), name='posts'),
    path('users/profile/<int:pk>', views.User.as_view(), name='profile'),
    path('users/profile-update/<int:pk>', views.UserUpdate.as_view(), name='profile_update'),
    path('posts/post-create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/post-update/<int:pk>', views.PostUpdate.as_view(), name='post-update'),
    path('posts/post-delete/<int:pk>', views.PostDelete.as_view(), name='post-delete'),
    path('accounts/signup/', views.Signup.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
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
