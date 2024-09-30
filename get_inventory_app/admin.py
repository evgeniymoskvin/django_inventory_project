from django.contrib import admin
from .models import GeneralInfoInventoryNumberModel, CloseInventoryNumbersModel, OpenInventoryNumbersModel, \
    KTInventoryNumbersModel, TypeOfInventoryNumberModel


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

admin.site.register(GeneralInfoInventoryNumberModel, GeneralInfoInventoryNumberAdmin)
admin.site.register(CloseInventoryNumbersModel, CloseInventoryNumbersAdmin)
admin.site.register(OpenInventoryNumbersModel, OpenInventoryNumbersAdmin)
admin.site.register(KTInventoryNumbersModel, KTInventoryNumbersAdmin)
admin.site.register(TypeOfInventoryNumberModel, TypeOfInventoryNumberAdmin)
