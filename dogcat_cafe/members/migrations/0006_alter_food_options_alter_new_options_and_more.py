# Generated by Django 5.0.1 on 2024-01-07 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_food_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='food',
            options={'ordering': ['id'], 'verbose_name': 'อาหาร', 'verbose_name_plural': 'รายการอาหาร'},
        ),
        migrations.AlterModelOptions(
            name='new',
            options={'ordering': ['id'], 'verbose_name': 'ข่าวสาร', 'verbose_name_plural': 'ข่าวสาร'},
        ),
        migrations.AlterModelOptions(
            name='pet',
            options={'ordering': ['id'], 'verbose_name': 'สัตว์เลี้ยง', 'verbose_name_plural': 'รายการสัตว์เลี้ยง'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['id'], 'verbose_name': 'โปรไฟล์', 'verbose_name_plural': 'โปรไฟล์'},
        ),
    ]
