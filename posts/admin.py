from django.contrib import admin
from posts.models import Post, User
from .forms import UserUpdateForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    form = UserUpdateForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    ordering = ('email',)
    filter_horizontal = ()


# admin.site.register(User)


@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'user_name', 'comment', 'web_site', 'profile_image', 'phone_number',
                    'gender', 'is_active', 'is_admin', 'last_login']
    list_display_links = ['email']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'image']
    list_display_links = ['content']
