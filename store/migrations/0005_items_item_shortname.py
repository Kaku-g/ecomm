# Generated by Django 3.1.1 on 2020-09-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200921_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='item_shortname',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
