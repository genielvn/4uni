# Generated by Django 4.2.11 on 2024-07-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_reply_body_alter_thread_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]