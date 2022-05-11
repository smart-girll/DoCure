# Generated by Django 4.0.3 on 2022-05-11 16:25

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=15)),
                ('height', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.datetime(2022, 5, 11, 21, 55, 51, 779652))),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cbc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rbc', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('wbc', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('pc', models.FloatField(blank=True, default=None, max_length=25, null=True)),
                ('hgb', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('rcd', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('mchc', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('mpv', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('pcv', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('mcv', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('name', models.CharField(max_length=150, null=True)),
                ('password', models.CharField(blank=True, max_length=150, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 5, 11, 21, 55, 51, 779652))),
                ('image', models.ImageField(default=None, null=True, upload_to='')),
                ('file', models.FileField(default=None, null=True, upload_to='')),
                ('rbc_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('wbc_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('pc_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('hgb_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('rcd_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('mchc_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('mpv_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('pcv_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('mcv_enc', models.BinaryField(default=None, editable=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmDoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('Surname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=250, unique=True)),
                ('phone_number', models.CharField(max_length=17, unique=True)),
                ('Specialization', models.CharField(choices=[('Orthopedics', 'Orthopedics'), (' Internal Medicine', ' Internal Medicine'), ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'), ('Dermatology', 'Dermatology'), ('Pediatrics', 'Pediatrics'), ('General Surgery', 'General Surgery'), ('Radiology', 'Radiology'), ('Ophthalmology', 'Ophthalmology'), (' Family Medicine', ' Family Medicine'), ('ENT', 'ENT')], max_length=500)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ViewDoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.confirmdoctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Urine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 5, 11, 21, 55, 51, 779652))),
                ('image', models.ImageField(default=None, null=True, upload_to='')),
                ('file', models.FileField(default=None, null=True, upload_to='')),
                ('glucose', models.CharField(default=None, max_length=150, null=True)),
                ('ketones', models.CharField(default=None, max_length=150, null=True)),
                ('reaction', models.CharField(default=None, max_length=150, null=True)),
                ('sg', models.FloatField(blank=True, default=None, max_length=150, null=True)),
                ('uro', models.CharField(default=None, max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='tempFileStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default=None, null=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, null=True, upload_to='')),
                ('file', models.FileField(default=None, null=True, upload_to='')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 5, 11, 21, 55, 51, 779652))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='confirmdoctor',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.doctor'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.TextField(max_length=500)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.confirmdoctor')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.cbc')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
