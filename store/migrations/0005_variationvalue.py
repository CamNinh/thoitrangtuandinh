# Generated by Django 4.0 on 2022-01-19 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_productimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation', models.CharField(choices=[('size', 'size'), ('color', 'color')], max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
