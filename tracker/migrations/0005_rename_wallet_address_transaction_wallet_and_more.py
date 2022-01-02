# Generated by Django 4.0 on 2022-01-01 19:58

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_remove_wallet_heroes_remove_wallet_lp_balance_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='wallet_address',
            new_name='wallet',
        ),
        migrations.AddField(
            model_name='wallet',
            name='crystal_log',
            field=jsonfield.fields.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='wallet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='created_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
