from rest_framework import serializers
from .models import Post, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'user_name', 'profile_image')


class PostUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'create_dt', 'updated_at', 'image', 'user')

    @classmethod
    def setup_prepending(cls, queryset):
        return queryset.select_related('user')

