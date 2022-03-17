# Generated by Django 4.0 on 2022-01-01 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0041_bookinstance_imprint_de_bookinstance_imprint_en_us_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name_de',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='room',
            name='name_en_us',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
