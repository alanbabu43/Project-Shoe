# Generated by Django 4.2.1 on 2023-06-29 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.FloatField(null=True),
        ),
    ]