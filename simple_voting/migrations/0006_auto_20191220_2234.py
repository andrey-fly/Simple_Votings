# Generated by Django 3.0 on 2019-12-20 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_voting', '0005_auto_20191220_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='author',
            field=models.IntegerField(default=0),
        ),
    ]
