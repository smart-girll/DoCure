# Generated by Django 4.0.3 on 2022-05-14 12:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_cbc_date_alter_filestore_date_alter_urine_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cbc',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 14, 18, 1, 7, 3791)),
        ),
        migrations.AlterField(
            model_name='filestore',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 14, 18, 1, 7, 7780)),
        ),
        migrations.AlterField(
            model_name='urine',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 14, 18, 1, 7, 8785)),
        ),
        migrations.AlterField(
            model_name='user',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 14, 18, 1, 6, 994967)),
        ),
    ]