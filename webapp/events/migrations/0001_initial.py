# Generated by Django 3.2 on 2021-11-08 23:51

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('logo', models.ImageField(upload_to='images/logos')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=7)),
                ('material_icon', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('body', models.CharField(max_length=10000, null=True)),
                ('organiser_name', models.CharField(max_length=100, null=True)),
                ('organiser_email', models.EmailField(max_length=255, null=True)),
                ('datetime_start', models.DateTimeField()),
                ('datetime_end', models.DateTimeField()),
                ('timezone', timezone_field.fields.TimeZoneField()),
                ('external', models.URLField(null=True)),
                ('supporters', models.ManyToManyField(to='events.Supporter')),
                ('tags', models.ManyToManyField(to='events.Tag')),
            ],
        ),
    ]
