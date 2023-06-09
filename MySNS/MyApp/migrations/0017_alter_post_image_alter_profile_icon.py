# Generated by Django 4.1.2 on 2023-04-04 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MyApp", "0016_alter_profile_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                default="post_images/D.jpg", upload_to="post_images/"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="icon",
            field=models.ImageField(
                blank=True,
                default="icons/default_icon.jpeg",
                null=True,
                upload_to="icons/",
            ),
        ),
    ]
