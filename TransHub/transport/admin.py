from django.contrib import admin
from .models import *


class LoadUnloadAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


admin.site.register(LoadUnload, LoadUnloadAdmin)
admin.site.register(Permissions, PermissionsAdmin)
admin.site.register(BodyType, BodyTypeAdmin)
