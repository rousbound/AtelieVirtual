# Generated by Django 3.0.5 on 2020-08-23 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pl',
            name='localdata',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
