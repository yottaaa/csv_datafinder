# Generated by Django 3.2.5 on 2021-07-14 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdf_app', '0002_auto_20210714_0319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvdata',
            old_name='data_filename',
            new_name='data_name',
        ),
    ]
