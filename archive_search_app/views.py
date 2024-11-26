from django.shortcuts import render, redirect
from django.views import View
from dotenv import load_dotenv
import tempfile
import requests
import os
import logging
from django.utils.decorators import method_decorator
# from django.core.files.temp import TemporaryFile, NamedTemporaryFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from get_inventory_app.models import OrdersModel, ObjectModel, EmployeeModel, CpeModel, TypeOfInventoryNumberModel, \
    OpenInventoryNumbersModel, GeneralInfoInventoryNumberModel, CloseInventoryNumbersModel, \
    GeneralInfoPermissionNumberModel, ReplacementPermissionNumbersModel, TypeOfPermissionNumberModel, \
    PermissionNumbersModel, ArchiveFilesModel, LogsDownloadsAlbum

load_dotenv()
API_ADDRESS_ARCHIVE = os.getenv('API_ADDRESS_ARCHIVE')
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


# Create your views here.
class SearchInArchiveView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        content = {

        }
        return render(request, 'archive_search_app/search_archive.html', content)

    def post(self, request):
        album = request.POST['search']
        search_result = None
        len_search_result = 0
        correct_album_len = False
        if len(album) >= 4:
            search_result = ArchiveFilesModel.objects.all().filter(album_name__icontains=album).order_by('album_name')
            len_search_result = len(search_result)
            correct_album_len = True

        content = {
            'search_word': request.POST['search'],
            'search_result': search_result,
            'len_search_result': len_search_result,
            'correct_album_len': correct_album_len
        }
        return render(request, 'archive_search_app/search_full_result.html', content)


class GetQuickSearchResultsView(View):
    """Выпадающий список с предложениями"""

    def post(self, request):
        print(f'request.POST: {request.POST}')
        search = request.POST['search']
        search_results = ArchiveFilesModel.objects.all().filter(album_name__icontains=search).order_by('album_name')[
                         :10]
        print(search_results)
        content = {
            'search_results': search_results,
        }
        return render(request, 'archive_search_app/ajax/quick_search_result.html', content)


class DownloadAlbumView(View):
    """Скачивание альбома"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        emp = EmployeeModel.objects.get(user=request.user)
        obj = ArchiveFilesModel.objects.get(id=pk)
        new_log = LogsDownloadsAlbum(download_file_key=obj,
                                     download_file_name=obj.album_name,
                                     download_emp_Key=emp,
                                     download_emp_name=f'{emp.last_name} {emp.first_name} {emp.middle_name}')
        new_log.save()
        file_name = obj.album_name
        file_name_split = file_name.split('.')
        if file_name_split[-1] == 'pdf':
            pdf_flag = True
        else:
            pdf_flag = False
        test_url = f'{API_ADDRESS_ARCHIVE}/download_album_api/{pk}'
        print(test_url)
        content = {
            'pdf_flag': pdf_flag,
            'file_name': obj.album_name,
            'test_url': test_url,
            'album_id': pk,
        }
        # return redirect(f'{API_ADDRESS_ARCHIVE}/download_album_api/{pk}')
        return render(request, 'archive_search_app/pdf_viewer.html', content)


class DownloadAlbumLinkView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        return redirect(f'{API_ADDRESS_ARCHIVE}/download_album_api/{pk}')