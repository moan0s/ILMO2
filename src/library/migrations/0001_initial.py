# Generated by Django 4.0 on 2022-03-17 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Date of death')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'ordering': ['last_name', 'first_name'],
                'permissions': (('can_modify_author', 'Can add, update or delete an author'),),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a book genre (e.g. Science Fiction)', max_length=200, verbose_name='Name')),
                ('name_en_us', models.CharField(help_text='Enter a book genre (e.g. Science Fiction)', max_length=200, null=True, verbose_name='Name')),
                ('name_de', models.CharField(help_text='Enter a book genre (e.g. Science Fiction)', max_length=200, null=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genre',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular item across whole library.', primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=20, unique=True, verbose_name='Label')),
                ('status', models.CharField(blank=True, choices=[('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='m', help_text='Item availability', max_length=1)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'permissions': (('can_mark_returned', 'Set item as returned'), ('can_see_borrowed', 'See all borrowed items')),
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a natural languages name (e.g. English, French, Japanese etc.).', max_length=200, unique=True)),
                ('languagecode', models.CharField(help_text='Enter the language code for this language. For further information see  http://www.i18nguy.com/unicode/language-identifiers.html', max_length=10, verbose_name='Language code')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lent_on', models.DateField(verbose_name='Lent on')),
                ('due_back', models.DateField(verbose_name='Due back')),
                ('returned_on', models.DateField(blank=True, null=True, verbose_name='Returned on')),
            ],
            options={
                'verbose_name': 'Loan',
                'verbose_name_plural': 'Loans',
                'permissions': (('can_add_loan', 'Can add a loan for all user'),),
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_en_us', models.CharField(max_length=200, null=True)),
                ('name_de', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this room', primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
                ('name_en_us', models.CharField(max_length=200, null=True, unique=True, verbose_name='Name')),
                ('name_de', models.CharField(max_length=200, null=True, unique=True, verbose_name='Name')),
                ('allowed_user', models.ManyToManyField(help_text='Users that are allowed to access this room.', to=settings.AUTH_USER_MODEL, verbose_name='Allowed user')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], verbose_name='Weekday')),
                ('from_hour', models.TimeField(verbose_name='From hour')),
                ('to_hour', models.TimeField(verbose_name='To hour')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='Comment')),
            ],
            options={
                'verbose_name': 'Opening hour',
                'verbose_name_plural': 'Opening hours',
                'ordering': ('weekday', 'from_hour'),
                'permissions': (('change_opening_hours', 'Can change opening hours'),),
                'unique_together': {('weekday', 'from_hour', 'to_hour')},
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.CharField(blank=True, help_text='The UID of a NFC chip (e.g. in a student id).', max_length=50, verbose_name='UID')),
                ('preferred_language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='library.language', verbose_name='Preffered language')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
        ),
        migrations.CreateModel(
            name='LoanReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_on', models.DateField(verbose_name='Sent on')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.loan', verbose_name='Loan')),
            ],
            options={
                'verbose_name': 'Loan Reminder',
                'verbose_name_plural': 'Loan Reminders',
            },
        ),
        migrations.AddField(
            model_name='loan',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.member', verbose_name='Borrower'),
        ),
        migrations.AddField(
            model_name='loan',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.item', verbose_name='Item'),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titel')),
                ('summary', models.TextField(help_text='Enter a brief description of the book.', max_length=1000, verbose_name='Summary')),
                ('isbn', models.CharField(help_text='ISBN number (13 Characters)', max_length=13, null=True, verbose_name='ISBN')),
                ('author', models.ManyToManyField(help_text='Select the autor(s) of this book.', to='library.Author', verbose_name='Author')),
                ('genre', models.ManyToManyField(help_text='Select a genre for this book.', to='library.Genre', verbose_name='Genre')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.language', verbose_name='Language')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='MaterialInstance',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='library.item')),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='library.material', verbose_name='Material')),
            ],
            options={
                'verbose_name': 'Material instance',
                'verbose_name_plural': 'Material instances',
            },
            bases=('library.item',),
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='library.item')),
                ('imprint', models.CharField(blank=True, max_length=200, null=True, verbose_name='Imprint')),
                ('imprint_en_us', models.CharField(blank=True, max_length=200, null=True, verbose_name='Imprint')),
                ('imprint_de', models.CharField(blank=True, max_length=200, null=True, verbose_name='Imprint')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='library.book', verbose_name='Book')),
            ],
            options={
                'verbose_name': 'Book instance',
                'verbose_name_plural': 'Book instances',
            },
            bases=('library.item',),
        ),
    ]
