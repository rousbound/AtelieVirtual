# Generated by Django 3.0.5 on 2020-08-23 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerj', '0003_auto_20200823_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pl',
            name='localdata',
            field=models.CharField(default='Governador', max_length=128, null=True),
        ),
    ]
