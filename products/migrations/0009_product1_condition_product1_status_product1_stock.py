# Generated by Django 4.2.5 on 2023-11-01 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_availability_sold_countdown_delete_offercount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product1',
            name='condition',
            field=models.CharField(choices=[('New', 'New'), ('Old', 'Old')], default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product1',
            name='status',
            field=models.CharField(choices=[('Publish', 'Publish'), ('Draft', 'Draft')], default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product1',
            name='stock',
            field=models.CharField(choices=[('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK')], default=1, max_length=200),
            preserve_default=False,
        ),
    ]