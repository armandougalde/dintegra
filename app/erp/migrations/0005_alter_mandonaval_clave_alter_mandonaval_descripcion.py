# Generated by Django 5.1 on 2024-10-10 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_mandonaval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandonaval',
            name='clave',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='mandonaval',
            name='descripcion',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
