# Generated by Django 5.0.4 on 2024-04-27 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
    ]