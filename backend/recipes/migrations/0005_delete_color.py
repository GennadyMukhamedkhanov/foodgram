# Generated by Django 4.0 on 2024-01-28 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_tag_color'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Color',
        ),
    ]