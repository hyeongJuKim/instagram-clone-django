from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': '사용자이름'}), label="")
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
        fields = ['username', 'password']


class UserCreateFrom(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '사용자이름'}), label="")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}), label="")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}), label="")

    def clean(self):
        cleaned_data = super(UserCreateFrom, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

    class Meta:
        model = User
        fields = ['username', 'password']
