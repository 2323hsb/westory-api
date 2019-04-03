from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Post, User, Story, UploadImage, Comment

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Profiles', {'fields': ('google_id', 'profile_img')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)
    filter_horizontal = ()

# admin.site.register(Post)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# admin.site.register(UploadImage)
admin.site.register(Story)
admin.site.register(Comment)