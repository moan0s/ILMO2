# Generated by Django 4.0 on 2022-03-16 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('library', '0037_alter_bookinstance_book'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='materialinstance',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AddField(
            model_name='item',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype'),
        ),
    ]
