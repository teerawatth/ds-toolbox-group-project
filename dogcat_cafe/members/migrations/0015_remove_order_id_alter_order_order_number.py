# Generated by Django 5.0.1 on 2024-01-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_alter_order_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.AutoField(default=1000, primary_key=True, serialize=False),
        ),
    ]
