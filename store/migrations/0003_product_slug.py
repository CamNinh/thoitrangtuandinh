# Generated by Django 4.0 on 2022-01-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]