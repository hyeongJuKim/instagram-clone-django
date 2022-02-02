from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.renderers import JSONRenderer

from posts import models
# from posts.mixins import AjaxFormMixin
from posts.mixins import AjaxFormMixin
from posts.module import send_find_password_email
from .models import Post, User, UserManager
from .forms import UserCreationForm, UserLoginForm, PostCreateForm, PostUpdateForm, UserUpdateForm
from django.urls import reverse_lazy

from .serialize import PostUserSerializer


class User(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/profile.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user).order_by('-create_dt')
        return queryset


def user_page(request):
    if request.method == 'GET':
        posts = models.Post.objects.filter(user=request.user)
        paginator = Paginator(posts, 1)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(page)
        except EmptyPage:
            posts = None

        serializer = PostUserSerializer(posts, many=True)

        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content, content_type="text/json-comment-filtered")


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = models.User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = "/users/profile-update/{id}"

    def get_queryset(self):
        queryset = models.User.objects.filter(email=self.request.user.email).order_by('-create_dt')
        return queryset


class Posts(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "object_list"
    template_name = 'posts/post_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-create_dt')


def posts_page(request):
    if request.method == 'GET':
        posts = models.Post.objects.filter(user=request.user).order_by('-create_dt')
        paginator = Paginator(posts, 1)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(paginator.page(1))
        except EmptyPage:
            posts = None

        serializer = PostUserSerializer(posts, many=True)

        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content, content_type="text/json-comment-filtered")


def post(request, pk):
    if request.method == 'GET':
        post = models.Post.objects.get(pk=pk)
        serializer = PostUserSerializer(post)
        content = JSONRenderer().render(serializer.data)

        return HttpResponse(content, content_type="text/json-comment-filtered")


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


class Explore(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "object_list"
    template_name = 'posts/explore.html'
    ordering = '-create_dt'
    paginate_by = 3


def explore_page(request):
    if request.method == 'GET':
        posts = models.Post.objects.filter().order_by('-create_dt')
        paginator = Paginator(posts, 1)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(paginator.page(1))
        except EmptyPage:
            posts = None

        serializer = PostUserSerializer(posts, many=True)

        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content, content_type="text/json-comment-filtered")


class Signup(AjaxFormMixin, FormView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class Login(View):
    form_class = UserLoginForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login.html'


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': models.User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


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
