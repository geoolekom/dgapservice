from .forms import AdminUserChangeForm, AdminUserAddForm
from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from feed.models import Post

class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm

    fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ( ('Personal info'), {'fields': (
        'first_name',
        'last_name',
        'email',
        'avatar',
    )}), )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'avatar')}
        ),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Post)