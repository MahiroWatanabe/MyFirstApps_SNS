# Generated by Django 4.1.2 on 2023-03-30 03:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("MyApp", "0008_talk_likes_alter_post_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="postlike",
            options={"verbose_name": "ポストいいね", "verbose_name_plural": "ポストいいね一覧"},
        ),
        migrations.AlterModelOptions(
            name="talklike",
            options={"verbose_name": "トークいいね", "verbose_name_plural": "トークいいね一覧"},
        ),
        migrations.AddField(
            model_name="post",
            name="views",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="talk",
            name="views",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name="talklike",
            unique_together={("talk", "user")},
        ),
    ]