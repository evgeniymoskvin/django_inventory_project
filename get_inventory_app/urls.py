"""
URL configuration for django_inventory_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('get-permission', views.GetPermissionView.as_view(), name='get-permission'),
    path('my_open_inventory_numbers', views.MyOpenInventoryNumbers.as_view(), name='my_open_inventory_numbers'),
    path('my_close_inventory_numbers', views.MyCloseInventoryNumbers.as_view(), name='my_close_inventory_numbers'),
    path('my_permission_numbers', views.MyPermissionNumbers.as_view(), name='my_permission_numbers'),
    path('my_replacement_permission_numbers', views.MyReplacementPermissionNumbers.as_view(), name='my_replacement_permission_numbers'),
    path('ajax/details-inventory-number-modal', views.DetailsInventoryNumberModalView.as_view(), name='details-modal'),
    path('ajax/details-permission-inventory-number-modal', views.DetailsPermissionNumberModalView.as_view(), name='details-permission-modal'),
    path('api/download_album/<int:pk>', views.DownloadAlbumView.as_view(), name='download-album'),
]
