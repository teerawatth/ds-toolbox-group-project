# Generated by Django 5.0.1 on 2024-01-07 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_foods_img_alter_pets_profile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Foods',
            new_name='Food',
        ),
        migrations.RenameModel(
            old_name='News',
            new_name='New',
        ),
        migrations.RenameModel(
            old_name='Pets',
            new_name='Pet',
        ),
    ]
