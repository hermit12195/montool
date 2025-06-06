# Generated by Django 4.2.20 on 2025-05-04 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_monuser_tg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='os_name',
            field=models.CharField(default='Linux', max_length=120),
        ),
        migrations.AlterField(
            model_name='server',
            name='health',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='status',
            field=models.CharField(blank=True, default='online', max_length=120, null=True),
        ),
    ]
