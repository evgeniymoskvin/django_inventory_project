import json
import os
import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import OrdersModel, ObjectModel, EmployeeModel, CpeModel, TypeOfInventoryNumberModel, \
    OpenInventoryNumbersModel, GeneralInfoInventoryNumberModel, CloseInventoryNumbersModel
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
        return render(request, 'get_inventory_app/index.html', content)

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
        cpe = CpeModel.objects.get_queryset().filter(cpe_object_id=object_id).filter(cpe_important=True).first()
        r = requests.post(f'{API_ADDRESS}/post', params={'order': f'{order_number}.{object_name}',
                                                         'employee': f'{employee.last_name} {employee.first_name[:1]}.{employee.middle_name[:1]}.',
                                                         'cpe': f'{cpe.cpe_user.last_name} {cpe.cpe_user.first_name[:1]}.{cpe.cpe_user.middle_name[:1]}',
                                                         'department': f'{employee.department.command_number}',
                                                         'phone': f'{employee.user_phone}',
                                                         'type_of_inventory_number': type_of_inventory_number})
        response_data = json.loads(r.text)
        print(type(response_data), response_data)
        # new_inventory =
        general_info = GeneralInfoInventoryNumberModel()
        general_info.order_id = order_id
        general_info.object_name_id = object_id
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
            return HttpResponse(status=400)
        content = {
            'new_inventory_number': new_inventory_number,
            'general_info': general_info
        }
        return render(request, 'get_inventory_app/ajax/get_inventory_done.html', content)
