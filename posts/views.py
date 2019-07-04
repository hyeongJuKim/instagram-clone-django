from django.views.generic import ListView, View, CreateView, UpdateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import UserCreateFrom, UserLoginForm, PostCreateForm, PostUpdateForm

from django.urls import reverse_lazy


class Posts(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        return queryset


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'
    success_url = '/'


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'posts/post_create.html'
    success_url = '/'


class Signup(CreateView):
    form_class = UserCreateFrom
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Login(View):
    form_class = UserLoginForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login.html'

