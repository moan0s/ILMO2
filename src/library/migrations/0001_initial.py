# Generated by Django 4.0 on 2022-03-17 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Died')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'permissions': (('can_modify_author', 'Can add, update or delete an author'),),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a book genre (e.g. Science Fiction)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular item across whole library', primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(blank=True, choices=[('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='m', help_text='Item availability', max_length=1)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'permissions': (('can_mark_returned', 'Set item as returned'), ('can_see_borrowed', 'See all borrowed items')),
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a natural languages name (e.g. English, French, Japanese etc.)', max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lent_on', models.DateField()),
                ('due_back', models.DateField()),
                ('returned_on', models.DateField(blank=True, null=True)),
            ],
            options={
                'permissions': (('can_add_loan', 'Can add a loan for all user'),),
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this room', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('allowed_user', models.ManyToManyField(help_text='Users that are allowed to access this room', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
                ('comment', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ('weekday', 'from_hour'),
                'permissions': (('change_opening_hours', 'Can change opening hours'),),
                'unique_together': {('weekday', 'from_hour', 'to_hour')},
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.CharField(blank=True, help_text='The UID of a NFC chip (e.g. in a student id)', max_length=50)),
                ('preferred_language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='library.language')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='LoanReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_on', models.DateField()),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.loan')),
            ],
        ),
        migrations.AddField(
            model_name='loan',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.member'),
        ),
        migrations.AddField(
            model_name='loan',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.item'),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(help_text='Enter a brief description of the book', max_length=1000)),
                ('isbn', models.CharField(help_text='ISBN number (13 Characters)', max_length=13, null=True, verbose_name='ISBN')),
                ('author', models.ManyToManyField(help_text='Select the autor(s) of this book', to='library.Author')),
                ('genre', models.ManyToManyField(help_text='Select a genre for this book', to='library.Genre')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.language')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialInstance',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='library.item')),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='library.material')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('library.item',),
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='library.item')),
                ('imprint', models.CharField(blank=True, max_length=200, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='library.book')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('library.item',),
        ),
    ]
