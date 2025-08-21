from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_user',"rating","comment","date")
    search_fields = ('user', "target_user",)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_user',"description","date")
    search_fields = ('user', "target_user",)

admin.site.register(User, UserAdmin)
admin.site.register(ActivityDirection)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Complaint, ComplaintAdmin)
