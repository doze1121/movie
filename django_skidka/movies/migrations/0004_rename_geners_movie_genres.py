# Generated by Django 4.2.2 on 2023-07-14 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_rename_ratig_rating_rename_revie_reviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='geners',
            new_name='genres',
        ),
    ]
