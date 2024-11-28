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
    path('', views.SearchInArchiveView.as_view(), name='search-in-archive'),
    path('search/ajax/quick_search', views.GetQuickSearchResultsView.as_view(), name='quick_search'),
    path('album/<int:pk>', views.DownloadAlbumView.as_view(), name='album'),
    path('download_album/<int:pk>', views.DownloadAlbumLinkView.as_view(), name='download-album'),
]
