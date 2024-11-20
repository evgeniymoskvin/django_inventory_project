from django.contrib import admin
from .models import GeneralInfoInventoryNumberModel, CloseInventoryNumbersModel, OpenInventoryNumbersModel, \
    KTInventoryNumbersModel, TypeOfInventoryNumberModel, TypeOfPermissionNumberModel, ReplacementPermissionNumbersModel, \
    GeneralInfoPermissionNumberModel, PermissionNumbersModel, ContractModel, ObjectModel, CpeModel, LogsDownloadsAlbum, ArchiveFilesModel


class GeneralInfoInventoryNumberAdmin(admin.ModelAdmin):
    ordering = ['-id']


class CloseInventoryNumbersAdmin(admin.ModelAdmin):
    ordering = ['-id']
    search_fields = ['general_info__employee']
    list_filter = ('general_info__order', 'general_info__object_name', 'actual')


class OpenInventoryNumbersAdmin(admin.ModelAdmin):
    ordering = ['-id']
    search_fields = ['general_info__employee']
    list_filter = ('general_info__order', 'general_info__object_name', 'actual')


class KTInventoryNumbersAdmin(admin.ModelAdmin):
    ordering = ['-id']
    search_fields = ['general_info__employee']
    list_filter = ('general_info__order', 'general_info__object_name', 'actual')


class TypeOfInventoryNumberAdmin(admin.ModelAdmin):
    ordering = ['number_of_code_in_ms_access']


class TypeOfPermissionNumberAdmin(admin.ModelAdmin):
    ordering = ['number_of_code_in_ms_access']
class ContractAdmin(admin.ModelAdmin):
    list_filter = ('contract_object', 'contract_code', 'contract_name', 'show')
    ordering = ['contract_object__object_code', 'contract_name', 'contract_code']

class ObjectAdmin(admin.ModelAdmin):
    list_filter = ('object_code', 'object_name')
    ordering = ['object_code', 'object_name']
class CpeAdmin(admin.ModelAdmin):
    search_fields = ['cpe_object', 'cpe_user']
    list_filter = ('cpe_user', 'cpe_object')
    ordering = ['cpe_object', 'cpe_user']
class ArchiveFilesAdmin(admin.ModelAdmin):
    search_fields = ['album_name', 'md5_file']
    list_filter = ('file_was_deleted', )
    ordering = ['album_name']
class LogsDownloadsAdmin(admin.ModelAdmin):
    search_fields = ['download_file_key', 'download_file_name', 'download_emp_name']
    ordering = ['-id']



admin.site.register(GeneralInfoInventoryNumberModel, GeneralInfoInventoryNumberAdmin)
admin.site.register(CloseInventoryNumbersModel, CloseInventoryNumbersAdmin)
admin.site.register(OpenInventoryNumbersModel, OpenInventoryNumbersAdmin)
admin.site.register(KTInventoryNumbersModel, KTInventoryNumbersAdmin)
admin.site.register(TypeOfInventoryNumberModel, TypeOfInventoryNumberAdmin)
admin.site.register(TypeOfPermissionNumberModel, TypeOfPermissionNumberAdmin)
admin.site.register(ContractModel, ContractAdmin)
admin.site.register(ObjectModel, ObjectAdmin)
admin.site.register(CpeModel, CpeAdmin)
admin.site.register(ArchiveFilesModel, ArchiveFilesAdmin)
admin.site.register(LogsDownloadsAlbum, LogsDownloadsAdmin)

