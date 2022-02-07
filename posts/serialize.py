from rest_framework import serializers
from .models import Post, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'user_name', 'profile_image')


class PostUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    create_dt_timesince = serializers.ReadOnlyField(source='timesince_format')

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'create_dt', 'create_dt_timesince', 'updated_at', 'image', 'user')

    @classmethod
    def setup_prepending(cls, queryset):
        return queryset.select_related('user')
