# Generated by Django 3.2.7 on 2021-09-11 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='autor',
            new_name='author',
        ),
    ]
