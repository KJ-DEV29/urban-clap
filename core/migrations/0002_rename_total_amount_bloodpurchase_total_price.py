# Generated by Django 5.2.4 on 2025-07-24 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodpurchase',
            old_name='total_amount',
            new_name='total_price',
        ),
    ]
