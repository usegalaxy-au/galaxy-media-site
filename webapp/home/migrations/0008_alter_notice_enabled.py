# Generated by Django 3.2 on 2021-12-02 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='enabled',
            field=models.BooleanField(default=False, help_text='Display on the Galaxy Australia landing page.'),
        ),
    ]
