from .forms import AdminUserChangeForm, AdminUserAddForm
from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm

    fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ( ('Personal info'), {'fields': (
        'first_name',
        'last_name',
        'email',
        'group',
        'avatar',
    )}), )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'group', 'email', 'password', 'avatar')}
        ),
    )

admin.site.register(User, UserAdmin)