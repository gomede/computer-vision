# Generated by Django 3.2.24 on 2024-02-17 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=17)),
                ('date', models.DateTimeField()),
                ('class_field', models.CharField(db_column='class', max_length=100)),
                ('evidence', models.TextField()),
            ],
        ),
    ]
