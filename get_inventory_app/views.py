import datetime
import json
import os
import logging

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import OrdersModel, ObjectModel, EmployeeModel, CpeModel, TypeOfInventoryNumberModel, \
    OpenInventoryNumbersModel, GeneralInfoInventoryNumberModel, CloseInventoryNumbersModel, \
    GeneralInfoPermissionNumberModel, ReplacementPermissionNumbersModel, TypeOfPermissionNumberModel, \
    PermissionNumbersModel, ArchiveFilesModel
from dotenv import load_dotenv
import requests
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

load_dotenv()
API_ADDRESS = os.getenv('API_ADDRESS')
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


# Create your views here.

class IndexView(View):
    """Главная страница"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        orders = OrdersModel.objects.all()
        objects = ObjectModel.objects.all().filter(show=True)
        type_of_inventory_number = TypeOfInventoryNumberModel.objects.all().order_by('number_of_code_in_ms_access')
        content = {
            'orders': orders,
            'objects': objects,
            'type_of_inventory_number': type_of_inventory_number
        }
        return render(request, 'get_inventory_app/get_inventory.html', content)

    def post(self, request):
        print(API_ADDRESS)
        # r = requests.get(f'{API_ADDRESS}/')
        print(f'request.POST: {request.POST}')
        print(f'request.user: {request.user}')
        employee = EmployeeModel.objects.get(user=request.user)
        order_id = int(request.POST['order_id'])
        order_number = OrdersModel.objects.get(id=order_id).order
        object_id = int(request.POST['object_id'])
        object_name = ObjectModel.objects.get(id=object_id).object_code
        type_of_inventory_number = int(request.POST['type_of_inventory_number'])
        count_of_inventory_number = int(request.POST['count_of_inventory_number'])
        final_inventory_list = []
        today_year_short = int(str(datetime.date.today().year)[-2:])

        try:
            cpe = CpeModel.objects.get_queryset().filter(cpe_object_id=object_id).filter(cpe_important=True).first()
            cpe_emp = cpe.cpe_user
            cpe_str = f'{cpe_emp.last_name} {cpe_emp.first_name[:1]}.{cpe_emp.middle_name[:1]}.'
        except Exception as e:
            cpe_emp = None
            print(e)
            cpe_str = 'Не указан'

        # Получение данных из БД
        # for i in range(count_of_inventory_number):
        #     general_info = GeneralInfoInventoryNumberModel()
        #     general_info.order_id = order_id
        #     general_info.object_name_id = object_id
        #     general_info.employee = employee
        #     general_info.cpe = cpe_emp
        #     general_info.save()
        #     if type_of_inventory_number == 1:
        #         # Открытый инвентарный номер
        #         new_inventory_number = OpenInventoryNumbersModel()
        #         last_inventory_number_from_db = OpenInventoryNumbersModel.objects.last()
        #         last_inventory_number_list = str(last_inventory_number_from_db.inventory_number).split('-')
        #         if int(last_inventory_number_list[0]) == today_year_short:
        #             last_inventory_number_str = str(int(last_inventory_number_list[1]) + 1)
        #             new_inventory_number.inventory_number = f'{today_year_short}-{last_inventory_number_str.rjust(5, "0")}'
        #         else:
        #             new_inventory_number.inventory_number = f'{today_year_short}-00001'
        #         new_inventory_number.general_info = general_info
        #         new_inventory_number.save()
        #         logging.info(f'Взят открытый номер {new_inventory_number.inventory_number}. {general_info.date_add}')
        #     elif type_of_inventory_number == 2:
        #         # Закрытый инвентарный номер
        #         new_inventory_number = CloseInventoryNumbersModel()
        #         last_close_inventory_number = CloseInventoryNumbersModel.objects.last()
        #         last_close_inventory_number_list = str(last_close_inventory_number.inventory_number).split('/')
        #         last_close_inventory_number_list_num = int(last_close_inventory_number_list[0])+1
        #         last_close_inventory_number_list_str = f'{str(last_close_inventory_number_list_num).rjust(5, "0")}'
        #         new_inventory_number.inventory_number = f'{last_close_inventory_number_list_str}/ДСП'
        #         new_inventory_number.general_info = general_info
        #         new_inventory_number.save()
        #         logging.info(f'Взят закрытый номер {new_inventory_number.inventory_number}. {general_info.date_add}')
        #     else:
        #         logging.warning(f'Тип документации {type_of_inventory_number} не найден')
        #         general_info.delete()
        #         return HttpResponse(status=500)
        #     print(new_inventory_number.inventory_number)
        #     final_inventory_list.append(new_inventory_number.inventory_number)

        # Получение инвентарного из БД access
        for i in range(count_of_inventory_number):
            r = requests.post(f'{API_ADDRESS}/post', params={'order': f'{order_number}.{object_name}',
                                                             'employee': f'{employee.last_name} {employee.first_name[:1]}.{employee.middle_name[:1]}.',
                                                             'cpe': cpe_str,
                                                             'department': f'{employee.department.command_number}',
                                                             'phone': f'{employee.user_phone}',
                                                             'type_of_inventory_number': type_of_inventory_number})
            response_data = json.loads(r.text)
            print(type(response_data), response_data)
            general_info = GeneralInfoInventoryNumberModel()
            general_info.order_id = order_id
            general_info.object_name_id = object_id
            general_info.cpe = cpe_emp
            general_info.employee = employee
            general_info.save()
            if type_of_inventory_number == 1:
                # Открытый инвентарный номер
                new_inventory_number = OpenInventoryNumbersModel()
                new_inventory_number.inventory_number = response_data['new_inventory']
                new_inventory_number.general_info = general_info
                new_inventory_number.save()
                logging.info(f'Взят открытый номер {new_inventory_number.inventory_number}. {general_info.date_add}')
            elif type_of_inventory_number == 2:
                # Закрытый инвентарный номер
                new_inventory_number = CloseInventoryNumbersModel()
                new_inventory_number.inventory_number = response_data['new_inventory']
                new_inventory_number.general_info = general_info
                new_inventory_number.save()
                logging.info(f'Взят закрытый номер {new_inventory_number.inventory_number}. {general_info.date_add}')
            else:
                logging.warning(f'Тип документации {type_of_inventory_number} не найден')
                general_info.delete()
                return HttpResponse(status=500)
            final_inventory_list.append(new_inventory_number.inventory_number)
        content = {
            'final_inventory_list': final_inventory_list,
            'count_inventory': len(final_inventory_list),
            'count_columns': len(final_inventory_list) // 20 + 1,
        }

        return render(request, 'get_inventory_app/ajax/get_inventory_done.html', content)


class MyOpenInventoryNumbers(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        employee = EmployeeModel.objects.get(user=request.user)
        # Открытые инвентарные номера
        open_employee_numbers = OpenInventoryNumbersModel.objects.all().filter(
            general_info__employee=employee).order_by('-id')
        content = {'open_employee_numbers': open_employee_numbers}
        return render(request, 'get_inventory_app/employee_open_inventory_numbers.html', content)


class MyCloseInventoryNumbers(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        employee = EmployeeModel.objects.get(user=request.user)
        # Открытые инвентарные номера
        open_employee_numbers = CloseInventoryNumbersModel.objects.all().filter(
            general_info__employee=employee).order_by('-id')
        content = {'open_employee_numbers': open_employee_numbers}
        return render(request, 'get_inventory_app/employee_close_inventory_numbers.html', content)


class DetailsInventoryNumberModalView(View):
    def get(self, request):
        print(request.GET.get('object'))
        object_id = int(request.GET.get('object'))
        if request.GET.get('type') == 'open':
            inventory_number_object = OpenInventoryNumbersModel.objects.get(id=object_id)
        elif request.GET.get('type') == 'close':
            inventory_number_object = CloseInventoryNumbersModel.objects.get(id=object_id)
        else:
            inventory_number_object = None
        content = {'obj': inventory_number_object,
                   }
        return render(request, 'get_inventory_app/ajax/details_inventory_number.html', content)


class GetPermissionView(View):
    """Главная страница"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        orders = OrdersModel.objects.all()
        objects = ObjectModel.objects.all().filter(show=True)
        type_of_permission_number = TypeOfPermissionNumberModel.objects.all().order_by('number_of_code_in_ms_access')
        content = {
            'orders': orders,
            'objects': objects,
            'type_of_permission_number': type_of_permission_number
        }
        return render(request, 'get_inventory_app/get_permission.html', content)

    def post(self, request):
        print(API_ADDRESS)
        print(f'request.POST: {request.POST}')
        employee = EmployeeModel.objects.get(user=request.user)
        order_id = int(request.POST['order_id'])
        order_number = OrdersModel.objects.get(id=order_id).order
        object_id = int(request.POST['object_id'])
        object_name = ObjectModel.objects.get(id=object_id).object_code
        type_of_permission_number = int(request.POST['type_of_permission_number'])
        try:
            cpe = CpeModel.objects.get_queryset().filter(cpe_object_id=object_id).filter(cpe_important=True).first()
            cpe_str = f'{cpe.cpe_user.last_name} {cpe.cpe_user.first_name[:1]}.{cpe.cpe_user.middle_name[:1]}'
        except Exception as e:
            print(e)
            cpe_str = 'Не указан'
        r = requests.post(f'{API_ADDRESS}/permission', params={'order': f'{order_number}.{object_name}',
                                                               'employee': f'{employee.last_name} {employee.first_name[:1]}.{employee.middle_name[:1]}.',
                                                               'cpe': cpe_str,
                                                               'department': f'{employee.department.command_number}',
                                                               'phone': f'{employee.user_phone}',
                                                               'type_of_permission_number': type_of_permission_number})
        response_data = json.loads(r.text)
        print(type(response_data), response_data)
        general_info = GeneralInfoPermissionNumberModel()
        general_info.order_id = order_id
        general_info.object_name_id = object_id
        general_info.employee = employee
        general_info.save()
        if type_of_permission_number == 1:
            # Номер разрешения
            new_permission_number = PermissionNumbersModel()
            new_permission_number.permission_number = response_data['new_permission']
            new_permission_number.general_info = general_info
            new_permission_number.save()
            logging.info(f'Взят номера разрешения {new_permission_number.permission_number}. {general_info.date_add}')
        elif type_of_permission_number == 3:
            # Номер разрешения на подмену
            new_permission_number = ReplacementPermissionNumbersModel()
            new_permission_number.permission_number = response_data['new_permission']
            new_permission_number.general_info = general_info
            new_permission_number.save()
            logging.info(
                f'Взят номер разрешения на подмену {new_permission_number.permission_number}. {general_info.date_add}')
        else:
            logging.warning(f'Тип документации {type_of_permission_number} не найден')
            general_info.delete()
            return HttpResponse(status=500)
        content = {
            'new_permission_number': new_permission_number,
            'general_info': general_info

        }
        return render(request, 'get_inventory_app/ajax/get_permission_done.html', content)


class MyPermissionNumbers(View):
    """Номера разрешений пользователя"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        employee = EmployeeModel.objects.get(user=request.user)
        # Открытые инвентарные номера
        permission_numbers = PermissionNumbersModel.objects.all().filter(
            general_info__employee=employee).order_by('-id')
        content = {'permission_numbers': permission_numbers}
        return render(request, 'get_inventory_app/employee_permission_numbers.html', content)


class MyReplacementPermissionNumbers(View):
    """Номера разрешений пользователя"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        employee = EmployeeModel.objects.get(user=request.user)
        # Открытые инвентарные номера
        replacement_permission_numbers = ReplacementPermissionNumbersModel.objects.all().filter(
            general_info__employee=employee).order_by('-id')
        content = {'replacement_permission_numbers': replacement_permission_numbers}
        return render(request, 'get_inventory_app/employee_replacement_permission_numbers.html', content)


class DetailsPermissionNumberModalView(View):
    def get(self, request):
        print(request.GET.get('object'))
        object_id = int(request.GET.get('object'))
        if request.GET.get('type') == 'open':
            inventory_number_object = OpenInventoryNumbersModel.objects.get(id=object_id)
        elif request.GET.get('type') == 'close':
            inventory_number_object = CloseInventoryNumbersModel.objects.get(id=object_id)
        else:
            inventory_number_object = None
        cpe = CpeModel.objects.get_queryset().filter(
            cpe_object_id=inventory_number_object.general_info.object_name_id).filter(cpe_important=True).first()
        content = {'obj': inventory_number_object,
                   'cpe': f'{cpe.cpe_user.last_name} {cpe.cpe_user.first_name[:1]}.{cpe.cpe_user.middle_name[:1]}'}
        return render(request, 'get_inventory_app/ajax/details_inventory_number.html', content)


