# Generated by Django 4.0.3 on 2022-05-04 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
