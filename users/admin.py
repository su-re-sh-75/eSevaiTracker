from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Document

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone_num', 'name', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['phone_num', 'name']
    fieldsets = (
        (None, {'fields': ('phone_num', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_num', 'name', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    add_form_template = None
    model = User

admin.site.register(User, UserAdmin)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['user', 'aadhaar_num', 'pan_num', 'voter_id']
    search_fields = ['user__phone_num', 'aadhaar_num', 'pan_num', 'voter_id']
