from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MenuItem)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'parent', 'named_url',)


admin.site.unregister(Group)
admin.site.unregister(User)
