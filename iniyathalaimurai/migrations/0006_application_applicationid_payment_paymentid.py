# Generated by Django 5.2.3 on 2025-06-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iniyathalaimurai', '0005_alter_payment_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='applicationID',
            field=models.CharField(blank=True, max_length=40, unique=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='paymentID',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
