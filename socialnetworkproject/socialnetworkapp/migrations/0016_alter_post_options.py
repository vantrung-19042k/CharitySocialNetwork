# Generated by Django 3.2.6 on 2021-09-15 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworkapp', '0015_remove_user_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_date']},
        ),
    ]