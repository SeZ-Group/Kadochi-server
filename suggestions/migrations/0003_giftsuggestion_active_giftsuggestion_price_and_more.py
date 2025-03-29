# Generated by Django 5.1.7 on 2025-03-29 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0002_remove_giftsuggestion_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftsuggestion',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='giftsuggestion',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='giftsuggestion',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='giftsuggestion',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='giftsuggestion',
            name='product_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='giftsuggestion',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='suggestions', to='suggestions.tag'),
        ),
    ]
