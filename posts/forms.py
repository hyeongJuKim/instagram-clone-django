from django import forms
from .models import User, Post
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': '사용자이름'}), label="")
        self.password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}), label="")

        class_update_fields = ['username', 'password']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': field_name
            })

    class Meta:
        model = User
        fields = ['email', 'password']


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'placeholder': '이메일 주소'}))
    name = forms.CharField(label='성명', widget=forms.TextInput(attrs={'placeholder': '성명'}))
    user_name = forms.CharField(label='사용자 이름', widget=forms.TextInput(attrs={'placeholder': '사용자 이름'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 재입력'}))

    class Meta:
        model = User
        fields = ('email','name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'name', 'user_name', 'profile_image', 'comment']


class PostCreateForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '문구 입력..'}), label="")

    class Meta:
        model = Post
        fields = ['user', 'content', 'image']


class PostUpdateForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '문구 입력..'}), label="")

    class Meta:
        model = Post
        fields = ['user', 'content']
