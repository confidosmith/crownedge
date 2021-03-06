# Generated by Django 4.0.3 on 2022-05-11 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0003_alter_booking_no_days_alter_booking_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='no_days',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('paid', models.BooleanField()),
                ('phone', models.CharField(max_length=50)),
                ('pay_code', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
