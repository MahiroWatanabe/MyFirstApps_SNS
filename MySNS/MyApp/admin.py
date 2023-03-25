from django.contrib import admin

from .models import Post, Talk

admin.site.register(Post)

admin.site.register(Talk)