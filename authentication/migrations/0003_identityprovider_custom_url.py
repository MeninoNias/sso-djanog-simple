# Generated by Django 4.2.10 on 2024-02-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_useridentity'),
    ]

    operations = [
        migrations.AddField(
            model_name='identityprovider',
            name='custom_url',
            field=models.CharField(blank=True, help_text='Custom URL o padrão é (/api/singin)', max_length=255, null=True),
        ),
    ]
