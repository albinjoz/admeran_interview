# Generated by Django 3.0.3 on 2021-05-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
