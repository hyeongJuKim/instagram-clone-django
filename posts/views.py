from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class Posts(LoginRequiredMixin, ListView):
    model = Post



