# Generated by Django 5.1 on 2024-10-10 19:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0005_alter_mandonaval_clave_alter_mandonaval_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='almacen',
            name='mando',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='almacenes', to='erp.mandonaval'),
        ),
    ]
