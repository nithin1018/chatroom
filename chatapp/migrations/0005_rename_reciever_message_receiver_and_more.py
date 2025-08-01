# Generated by Django 5.2.4 on 2025-08-02 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatapp", "0004_remove_message_user_message_reciever_message_sender"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="reciever",
            new_name="receiver",
        ),
        migrations.AlterField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sent",
                to="chatapp.profile",
            ),
        ),
    ]
