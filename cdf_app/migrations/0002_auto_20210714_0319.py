# Generated by Django 3.2.5 on 2021-07-14 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdf_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvdata',
            old_name='file',
            new_name='data_file',
        ),
        migrations.RenameField(
            model_name='csvdata',
            old_name='filename',
            new_name='data_filename',
        ),
        migrations.RenameField(
            model_name='csvdata',
            old_name='items',
            new_name='data_items',
        ),
    ]
