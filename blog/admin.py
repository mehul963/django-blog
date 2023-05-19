from django.contrib import admin

# Register your models here.

from .models import blog,User
@admin.register(blog)
class AuthorAdmin(admin.ModelAdmin):
    list_display_links=('slug',)
    list_display=('slug',)

admin.site.register(User)
