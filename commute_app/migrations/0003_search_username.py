# Generated by Django 4.1.7 on 2023-03-09 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commute_app', '0002_search_drivescore_search_groceryscore_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='username',
            field=models.CharField(default='no username', max_length=500),
        ),
    ]