# Generated by Django 2.0.4 on 2018-04-20 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_van_van_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='facility_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
