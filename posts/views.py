from django.views.generic import ListView
from .models import Post


class Posts(ListView):
    model = Post
