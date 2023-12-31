# Generated by Django 5.0.1 on 2024-01-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_alter_cart_options_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'ordering': ['id'], 'verbose_name': 'รายการ', 'verbose_name_plural': 'รายการในตะกร้า'},
        ),
        migrations.AddField(
            model_name='food',
            name='suggested',
            field=models.BooleanField(default=False),
        ),
    ]
