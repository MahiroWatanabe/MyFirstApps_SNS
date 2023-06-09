# Generated by Django 4.1.2 on 2023-03-30 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MyApp", "0009_alter_postlike_options_alter_talklike_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="image",
            new_name="image1",
        ),
        migrations.AddField(
            model_name="post",
            name="image2",
            field=models.ImageField(blank=True, null=True, upload_to="post_images/"),
        ),
        migrations.AddField(
            model_name="post",
            name="image3",
            field=models.ImageField(blank=True, null=True, upload_to="post_images/"),
        ),
        migrations.AddField(
            model_name="post",
            name="image4",
            field=models.ImageField(blank=True, null=True, upload_to="post_images/"),
        ),
        migrations.AddField(
            model_name="post",
            name="image5",
            field=models.ImageField(blank=True, null=True, upload_to="post_images/"),
        ),
    ]
