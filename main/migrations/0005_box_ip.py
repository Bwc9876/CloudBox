# Generated by Django 4.2.6 on 2023-10-22 05:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_box_name_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="box",
            name="ip",
            field=models.CharField(default="EMPTY", max_length=20),
            preserve_default=False,
        ),
    ]