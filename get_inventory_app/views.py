import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import OrdersModel, ObjectModel, EmployeeModel, CpeModel
from dotenv import load_dotenv
import requests
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

load_dotenv()
API_ADDRESS = os.getenv('API_ADDRESS')


# Create your views here.

class IndexView(View):
    """Главная страница"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        orders = OrdersModel.objects.all()
        objects = ObjectModel.objects.all().filter(show=True)
        content = {
            'orders': orders,
            'objects': objects
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
        cpe = CpeModel.objects.get_queryset().filter(cpe_object_id=object_id).filter(cpe_important=True).first()
        r = requests.post(f'{API_ADDRESS}/post', params={'order': f'{order_number}.{object_name}',
                                                         'employee': f'{employee.last_name} {employee.first_name[:1]}.{employee.middle_name[:1]}.',
                                                         'cpe': f'{cpe.cpe_user.last_name}',
                                                         'department': f'{employee.department.command_number}',
                                                         'phone': f'{employee.user_phone}'})
        print(r.text)
        return HttpResponse(r.text)
