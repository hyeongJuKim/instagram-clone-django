from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
] + find(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
