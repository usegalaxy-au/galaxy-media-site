# Generated by Django 4.0.3 on 2022-08-30 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    def set_is_tool_update_field(self, schema_editor):
        """Set is_tool_update field for appropriate news records."""
        News = self.get_model('news', 'News')
        for n in News.objects.filter(title__icontains="tool update"):
            n.is_tool_update = True
            n.save()

    dependencies = [
        ('news', '0011_alter_news_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='is_tool_update',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            set_is_tool_update_field,
            migrations.RunPython.noop,
        ),
    ]