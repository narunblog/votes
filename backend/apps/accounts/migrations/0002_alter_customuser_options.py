# Generated by Django 3.2.9 on 2022-09-08 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'CustomUser', 'verbose_name_plural': 'CustomUsers'},
        ),
    ]
