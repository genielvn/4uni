# Generated by Django 4.2.11 on 2024-07-02 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='body',
            field=models.TextField(blank=True, default='data changed'),
            preserve_default=False,
        ),
    ]
