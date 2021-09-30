# Generated by Django 3.2.6 on 2021-09-29 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworkapp', '0031_auto_20210929_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionitem',
            old_name='creator',
            new_name='user_sell',
        ),
        migrations.AlterField(
            model_name='action',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Haha'), (0, 'Like'), (3, 'Wow'), (1, 'Heart')], default=0),
        ),
    ]
