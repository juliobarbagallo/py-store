# Generated by Django 4.1.7 on 2023-03-10 18:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="OrderProductItem",
        ),
    ]
