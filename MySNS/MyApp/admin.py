from django.contrib import admin

from .models import Post, Talk, PostLike, TalkLike

admin.site.register(Post)

admin.site.register(Talk)

admin.site.register(PostLike)

admin.site.register(TalkLike)