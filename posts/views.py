from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from posts import models
from posts.module import send_find_password_email
from .models import Post
from .forms import UserCreationForm, UserLoginForm, PostCreateForm, PostUpdateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class User(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/profile.html'

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user).order_by('-create_dt')
        return queryset


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = models.User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = "/users/profile-update/{id}"


class Posts(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "object_list"
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-create_dt')


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


class PostDelete(DeleteView):
    model = Post
    success_url = '/'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class Signup(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Login(View):
    form_class = UserLoginForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login.html'


@csrf_exempt
def password_reset_request(request):
    if request.method == 'GET':
        return render(request, 'users/password_reset_request.html')

    elif request.method == 'POST':
        email = request.POST.get('email', '')
        user = models.User.objects.get(email=email)
        # 토큰 생성 > a tag까지 전달. email전송 할 때 param으로 담아
        status = send_find_password_email(email)
        return HttpResponse(status)


def password_reset_response(request, key):

    if request.method == 'GET':
        return render(request, 'users/password_reset.html')
