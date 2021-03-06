# Generated by Django 3.2 on 2022-02-25 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_notice_notice_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='notice_class',
            field=models.CharField(choices=[('info', 'info'), ('warning', 'warning'), ('danger', 'danger'), ('success', 'none')], default='', help_text='A style class to set a color schema for the notice.', max_length=16),
        ),
    ]
