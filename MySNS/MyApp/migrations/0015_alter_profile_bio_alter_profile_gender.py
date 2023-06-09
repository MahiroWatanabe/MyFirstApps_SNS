# Generated by Django 4.1.2 on 2023-04-03 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MyApp", "0014_alter_profile_posts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("非公開", "非公開"), ("男", "男"), ("女", "女"), ("その他", "その他")],
                max_length=4,
                null=True,
            ),
        ),
    ]
