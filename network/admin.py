from django.contrib import admin
from .models import User, Post

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id")
    filter_horizontal = ("followers", "following")

class PostAdmin(admin.ModelAdmin):
    list_display = ("creator", "content", "date", "id")
    filter_horizontal = ("liked_by",)
    

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)