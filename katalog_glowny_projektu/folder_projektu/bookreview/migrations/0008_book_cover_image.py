# Generated by Django 5.1.5 on 2025-01-18 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookreview', '0007_alter_review_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers/'),
        ),
    ]
