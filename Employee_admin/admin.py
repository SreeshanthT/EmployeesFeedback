from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User,Review

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','mobile_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Verification'), {'fields': ('is_verified_freelancer',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined',)
    list_filter = ('is_superuser', 'is_active')
    date_hierarchy = 'date_joined'
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass