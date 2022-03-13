# Generated by Django 4.0.3 on 2022-03-13 11:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='end_date',
            field=models.DateField(default=datetime.date(2022, 3, 13)),
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 3, 13)),
        ),
        migrations.CreateModel(
            name='TaskUpdates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_title', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('activity', models.TextField(blank=True, null=True)),
                ('updated_on', models.DateField(auto_now_add=True)),
                ('modifier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
