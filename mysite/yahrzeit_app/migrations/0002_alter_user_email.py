# Generated by Django 4.1.5 on 2023-01-10 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("yahrzeit_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=100),
        ),
    ]
