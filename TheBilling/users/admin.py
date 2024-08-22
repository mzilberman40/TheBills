from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import UserProfile, User



class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user"""
    ordering = ['id']
    list_display = ['email',]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'password1',
                       'password2',
                       'is_active',
                       'is_staff',
                       'is_superuser',
                       ),
        },
         ),
    )


admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')