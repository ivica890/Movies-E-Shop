# Generated by Django 4.2.2 on 2023-06-18 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw5', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='category',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
