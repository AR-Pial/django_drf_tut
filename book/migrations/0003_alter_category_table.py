# Generated by Django 5.0.4 on 2024-04-26 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_category_book_author_book_created'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='categories',
        ),
    ]