# Generated by Django 2.2.1 on 2019-05-22 18:00

from django.db import models, migrations
from wagtail.core.rich_text import RichText


def convert_to_streamfield(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    for page in BlogPage.objects.all():
        if hasattr(page.body, 'raw_text') and page.body.raw_text and not page.body:
            page.body = [('rich_text', RichText(page.body.raw_text))]
            page.save()


def convert_to_richtext(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    for page in BlogPage.objects.all():
        if not hasattr(page.body, 'raw_text') or page.body.raw_text is None:
            raw_text = ''.join([
                child.value.source for child in page.body
                if child.block_type == 'rich_text'
            ])
            page.body = raw_text
            page.save()




class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpagegalleryimage'),
    ]

    operations = [
        migrations.RunPython(convert_to_streamfield, convert_to_richtext)
    ]