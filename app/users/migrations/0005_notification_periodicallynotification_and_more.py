# Generated by Django 4.2.9 on 2024-02-02 21:49

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_telegramuser_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", ckeditor.fields.RichTextField(blank=True, max_length=1023, null=True)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Создан"), (1, "Отработан"), (2, "В процессе")], default=0, editable=False
                    ),
                ),
                ("all_chats", models.IntegerField(default=0, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
            ],
            options={
                "verbose_name": "Оповещение ",
                "verbose_name_plural": "Оповещения ",
            },
        ),
        migrations.CreateModel(
            name="PeriodicallyNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", ckeditor.fields.RichTextField(blank=True, max_length=1023, null=True)),
                ("is_current", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
            ],
            options={
                "verbose_name": "Периодическое оповещение ",
                "verbose_name_plural": "Периодическое оповещения ",
            },
        ),
        migrations.CreateModel(
            name="PeriodicallyNotificationShots",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="notification", verbose_name="Изображеение")),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="periodic_shots",
                        to="users.periodicallynotification",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение периодического оповещения ",
                "verbose_name_plural": "Изображения периодического оповещения ",
            },
        ),
        migrations.CreateModel(
            name="NotificationShots",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="notification", verbose_name="Изображеение")),
                (
                    "notification",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.notification"),
                ),
            ],
            options={
                "verbose_name": "Изображение оповещения ",
                "verbose_name_plural": "Изображения оповещения ",
            },
        ),
    ]
