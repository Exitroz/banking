# Generated by Django 4.2.1 on 2023-06-03 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_transaction_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='receiver_name',
            new_name='account_name',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='receiver_number',
            new_name='account_number',
        ),
        migrations.AddField(
            model_name='transaction',
            name='bank_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
