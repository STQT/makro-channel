# Generated by Django 4.2.9 on 2024-01-30 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramUser",
            fields=[
                (
                    "id",
                    models.PositiveBigIntegerField(
                        db_index=True, editable=False, primary_key=True, serialize=False, verbose_name="Телеграм ID"
                    ),
                ),
                ("language", models.CharField(blank=True, max_length=2, null=True, verbose_name="Язык пользователя")),
                ("fullname", models.CharField(blank=True, max_length=100, null=True, verbose_name="Имя пользователя")),
                ("phone", models.CharField(blank=True, max_length=20, null=True, verbose_name="Телефонный номер")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
