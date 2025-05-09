# Generated by Django 4.2.17 on 2025-04-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_rating_chair_rating_source_rating_source_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chair',
            name='city',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chair',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chair',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chair',
            name='road',
            field=models.CharField(blank=True, null=True),
        ),
    ]
