from django.contrib import admin

from posts.models import Like
from posts.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
