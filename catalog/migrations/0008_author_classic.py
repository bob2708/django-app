# Generated by Django 3.2.8 on 2021-11-16 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_stih__checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='classic',
            field=models.BooleanField(default=False),
        ),
    ]
