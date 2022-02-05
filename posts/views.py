from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.renderers import JSONRenderer
from posts import models
from posts.mixins import AjaxFormMixin
from posts.module import send_find_password_email
from .models import Post
from .forms import UserCreationForm, UserLoginForm, PostCreateForm, PostUpdateForm, UserUpdateForm
from django.urls import reverse_lazy
from .serialize import PostUserSerializer


class User(LoginRequiredMixin, ListView):
    """ 프로필 페이지 이동 """
    model = Post
    template_name = 'posts/profile.html'
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        tot_cnt = self.model.objects.count()
        object_list = Post.objects.filter(user=self.request.user).order_by('-create_dt')

        return render(request, self.template_name, {'object_list': object_list, 'tot_cnt': tot_cnt})


def user_page(request):
    """ 프로필 게시물 조회 """

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
    """ 프로필 수정 """
    model = models.User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = "/users/profile-update/{id}"

    def get_queryset(self):
        queryset = models.User.objects.filter(email=self.request.user.email)
        return queryset


class Posts(LoginRequiredMixin, ListView):
    """ 게시글 목록 화면 """

    model = Post
    context_object_name = "object_list"
    template_name = 'posts/post_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-create_dt')


def posts_page(request):
    """ 게시글 목록 조회 """

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


@csrf_exempt
def post(request, pk):
    """ 게시글 조회 """

    post = models.Post.objects.get(pk=pk)

    # 단일 페이지
    if request.method == 'GET':
        return render(request, 'posts/post.html', {'post': post})

    # 포스트 내용 조회
    if request.method == 'POST':
        serializer = PostUserSerializer(post)
        content = JSONRenderer().render(serializer.data)

        return HttpResponse(content, content_type="text/json-comment-filtered")


class PostCreate(LoginRequiredMixin, CreateView):
    """ 게시글 생성 """

    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'
    success_url = '/'


class PostUpdate(LoginRequiredMixin, UpdateView):
    """ 게시글 수정 """

    model = Post
    form_class = PostUpdateForm
    template_name = 'posts/post_create.html'
    success_url = '/'


class PostDelete(DeleteView):
    """ 게시글 삭제 """

    model = Post
    success_url = '/'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class Explore(LoginRequiredMixin, ListView):
    """ 게시물 탐색 페이지 이동 """

    model = Post
    context_object_name = "object_list"
    template_name = 'posts/explore.html'
    ordering = '-create_dt'
    paginate_by = 9


def explore_page(request):
    """ 게시물 탐색 조회 """

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
