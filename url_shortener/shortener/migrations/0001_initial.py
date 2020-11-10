# Generated by Django 3.1.3 on 2020-11-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2048)),
                ('click_count', models.PositiveIntegerField(default=0)),
                ('date_created', models.DateTimeField()),
            ],
        ),
    ]
