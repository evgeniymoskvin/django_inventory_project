import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import OrdersModel, ObjectModel
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
        order_id = int(request.POST['order_id'])
        name_of_data = OrdersModel.objects.get(id=order_id).order_name
        print(name_of_data)
        r = requests.post(f'{API_ADDRESS}/post', params={'order': name_of_data,
                                                         'employee': 'employee ',
                                                         'cpe': 'cpe',
                                                         'department': 'department',
                                                         'phone': 6969})
        print(r.text)
        return HttpResponse(r.text)
