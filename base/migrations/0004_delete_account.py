# Generated by Django 4.2.1 on 2023-06-01 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_transaction_receiver_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
