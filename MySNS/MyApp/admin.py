from django.contrib import admin

from .models import Post, Talk, PostLike

admin.site.register(Post)

admin.site.register(Talk)

admin.site.register(PostLike)