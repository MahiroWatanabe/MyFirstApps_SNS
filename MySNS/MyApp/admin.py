from django.contrib import admin

from .models import Post, Talk, PostLike, TalkLike, Profile

admin.site.register(Post)
admin.site.register(Talk)
admin.site.register(PostLike)
admin.site.register(TalkLike)
admin.site.register(Profile)