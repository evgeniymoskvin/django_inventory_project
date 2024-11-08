# Generated by Django 5.1.1 on 2024-10-30 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_inventory_app', '0005_alter_typeofpermissionnumbermodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalinfopermissionnumbermodel',
            name='cpe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cpe_perm_employee', to='get_inventory_app.employeemodel', verbose_name='ГИП'),
        ),
        migrations.AlterField(
            model_name='generalinfopermissionnumbermodel',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emp_perm_employee', to='get_inventory_app.employeemodel', verbose_name='Сотрудник'),
        ),
    ]
