# Generated by Django 3.2.6 on 2021-09-29 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworkapp', '0022_auto_20210929_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Wow'), (0, 'Like'), (1, 'Heart'), (2, 'Haha')], default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]