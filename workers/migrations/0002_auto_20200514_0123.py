# Generated by Django 3.0.5 on 2020-05-13 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0008_auto_20200501_1403'),
        ('workers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workers',
            name='block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institute.Blocks'),
        ),
    ]
