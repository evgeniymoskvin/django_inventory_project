# Generated by Django 5.1.1 on 2024-10-22 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_inventory_app', '0003_alter_typeofinventorynumbermodel_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeOfPermissionNumberModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_type', models.CharField(max_length=100, verbose_name='Название разрешения')),
                ('number_of_code_in_ms_access', models.IntegerField(verbose_name='КодТипДокИзм в MS Access')),
            ],
            options={
                'verbose_name': 'тип инвентарного номера',
                'verbose_name_plural': 'типы инвентарных номеров',
            },
        ),
        migrations.CreateModel(
            name='GeneralInfoPermissionNumberModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_add', models.DateField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('return_date', models.DateField(blank=True, null=True, verbose_name='Дата возврата')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='get_inventory_app.employeemodel', verbose_name='Сотрудник')),
                ('object_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='get_inventory_app.objectmodel', verbose_name='Объект')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='get_inventory_app.ordersmodel', verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'общая информация о номере разрешения',
                'verbose_name_plural': 'общая информация о номерах разрешений',
            },
        ),
        migrations.CreateModel(
            name='PermissionNumbersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_number', models.CharField(max_length=8, verbose_name='Номер разрешения')),
                ('actual', models.BooleanField(default=True, verbose_name='Актуальный')),
                ('general_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='get_inventory_app.generalinfopermissionnumbermodel', verbose_name='Общая информация')),
            ],
            options={
                'verbose_name': 'открытый инвентарный номер',
                'verbose_name_plural': 'открытие инвентарные номера',
            },
        ),
        migrations.CreateModel(
            name='ReplacementPermissionNumbersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_number', models.CharField(max_length=8, verbose_name='Номер разрешения на подмену')),
                ('actual', models.BooleanField(default=True, verbose_name='Актуальный')),
                ('general_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='get_inventory_app.generalinfopermissionnumbermodel', verbose_name='Общая информация')),
            ],
            options={
                'verbose_name': 'открытый инвентарный номер',
                'verbose_name_plural': 'открытие инвентарные номера',
            },
        ),
    ]