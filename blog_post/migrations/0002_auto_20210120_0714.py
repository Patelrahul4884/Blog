# Generated by Django 3.1.3 on 2021-01-20 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.EmailField(max_length=254),
        ),
    ]
