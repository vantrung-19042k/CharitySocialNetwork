# Generated by Django 3.2.6 on 2021-09-29 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworkapp', '0026_auto_20210929_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Haha'), (1, 'Heart'), (0, 'Like'), (3, 'Wow')], default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]