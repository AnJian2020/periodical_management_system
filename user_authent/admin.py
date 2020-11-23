from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import UserInformation,UserMenuModel

admin.site.register(UserInformation)
admin.site.register(Permission)
# admin.site.register(UserMenuModel)

@admin.register(UserMenuModel)
class UserMenuAdmin(admin.ModelAdmin):
    list_display = ['id','menu_name','menu_level','parent_menu']