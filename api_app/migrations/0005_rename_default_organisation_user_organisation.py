# Generated by Django 5.0.6 on 2024-07-07 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0004_rename_organisation_user_default_organisation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='default_organisation',
            new_name='organisation',
        ),
    ]
