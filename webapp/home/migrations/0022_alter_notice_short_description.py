# Generated by Django 4.0.3 on 2022-11-29 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_notice_short_description_alter_notice_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='short_description',
            field=models.CharField(help_text='This will be displayed on the landing page (max 200 chars). Plain text or inline HTML e.g. &lt;b&gt;, &lt;img&gt;. Will be diplayed with a max height of 100px.', max_length=200),
        ),
    ]
