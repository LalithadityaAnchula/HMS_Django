# Generated by Django 3.0.5 on 2020-05-13 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institute', '0008_auto_20200501_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('staff_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('designation', models.CharField(choices=[('Scavenger', 'Scavenger'), ('General Servant', 'General Servant'), ('Doctor', 'Doctor'), ('Electrician', 'Electrician'), ('Firefighter', 'Firefighter'), ('Gym Trainer', 'Gym Trainer'), ('PT/Games Coach', 'PT/Games Coach')], max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('email_id', models.CharField(max_length=50, null=True)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='institute.Blocks')),
            ],
        ),
    ]