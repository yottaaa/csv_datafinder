# Generated by Django 3.2.5 on 2021-07-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdf_app', '0004_alter_csvdata_data_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvdata',
            name='data_file',
            field=models.TextField(blank=True),
        ),
    ]