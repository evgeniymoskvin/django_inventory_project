from os import path

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractUser


# Create your models here.

class OrdersModel(models.Model):
    """    Таблица номеров заказов    """
    order = models.CharField("Номер заказчика", null=True, max_length=10, blank=True)
    order_name = models.CharField(verbose_name="Наименование заказчика", null=True, blank=True, max_length=250)

    class Meta:
        verbose_name = _("номер заказчика")
        verbose_name_plural = _("номера заказчиков")
        managed = False
        db_table = 'ToDo_tasks_ordersmodel'

    def __str__(self):
        return f'{self.order} - {self.order_name}'


class ObjectModel(models.Model):
    """Таблица с наименованиями объектов"""
    object_name = models.CharField("Наименование объекта", max_length=250, default=None)
    object_code = models.CharField(verbose_name="Код объекта", max_length=10, null=True, blank=True)
    show = models.BooleanField("Отображать объект", default=True)

    class Meta:
        verbose_name = _("наименование объекта")
        verbose_name_plural = _("наименования объектов")
        managed = False
        db_table = 'ToDo_tasks_objectmodel'

    def __str__(self):
        return f'{self.object_code} - {self.object_name}'


class ContractModel(models.Model):
    """Таблица договоров"""
    contract_object = models.ForeignKey(ObjectModel, on_delete=models.PROTECT, verbose_name="Объект", default=1)
    contract_name = models.CharField(max_length=650, verbose_name="Номер договора")
    contract_code = models.CharField(max_length=500, verbose_name="Код договора", null=True, blank=True)
    show = models.BooleanField("Отображать договор", default=True)
    show_in_print = models.BooleanField("Отображать только в печати", default=False)

    class Meta:
        verbose_name = _("номер договора")
        verbose_name_plural = _("номера договоров")
        managed = False
        db_table = 'ToDo_tasks_contractmodel'

    def __str__(self):
        return f'{self.contract_object}, {self.contract_name}'


class JobTitleModel(models.Model):
    """ Таблица должностей """

    job_title = models.CharField("Должность", max_length=200)

    class Meta:
        verbose_name = _("должность")
        verbose_name_plural = _("должности")
        managed = False
        db_table = 'ToDo_tasks_jobtitlemodel'

    def __str__(self):
        return f'{self.job_title}'


class CityDepModel(models.Model):
    """Таблица городов"""
    city = models.CharField(verbose_name="Город", max_length=100)
    name_dep = models.CharField(verbose_name="Наименование организации", max_length=350)

    class Meta:
        managed = False
        verbose_name = _("город/организация")
        verbose_name_plural = _("города/организации")
        db_table = 'admin_panel_app_citydepmodel'

    def __str__(self):
        return f'{self.city} - {self.name_dep}'


class GroupDepartmentModel(models.Model):
    """Таблица управлений"""
    group_dep_abr = models.CharField("Сокращенное название управления", max_length=10)
    group_dep_name = models.CharField("Полное название управления", max_length=250)
    city_dep = models.ForeignKey(CityDepModel, verbose_name="Город", on_delete=models.SET_NULL, null=True, blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.group_dep_abr}, {self.group_dep_name}'

    class Meta:
        verbose_name = _("управление")
        verbose_name_plural = _("управления")
        managed = False
        db_table = 'ToDo_tasks_groupdepartmentmodel'


class CommandNumberModel(models.Model):
    """Таблица отделов"""
    command_number = models.IntegerField("Номер отдела/Сокращение")
    command_name = models.CharField("Наименование отдела", max_length=150)
    department = models.ForeignKey(GroupDepartmentModel, verbose_name="Управление", on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.command_number}, {self.command_name}'

    class Meta:
        verbose_name = _("номер отдела")
        verbose_name_plural = _("номера отделов")
        managed = False
        db_table = 'ToDo_tasks_commandnumbermodel'


class EmployeeModel(models.Model):
    """Таблица сотрудников"""
    user = models.OneToOneField(User, models.PROTECT, verbose_name="Пользователь", related_name='phonebook_emp_user')
    last_name = models.CharField("Фамилия", max_length=150)
    first_name = models.CharField("Имя", max_length=150)
    middle_name = models.CharField("Отчество", max_length=150)
    personnel_number = models.CharField("Табельный номер", max_length=20, null=True, default=None)
    job_title = models.ForeignKey(JobTitleModel, on_delete=models.PROTECT, null=True, verbose_name="Должность")
    department = models.ForeignKey(CommandNumberModel, on_delete=models.PROTECT, null=True, verbose_name="№ отдела")
    user_phone = models.IntegerField("№ телефона внутренний", null=True, default=None, blank=True)
    department_group = models.ForeignKey(GroupDepartmentModel, on_delete=models.SET_NULL, default=None, null=True,
                                         verbose_name="Управление")
    right_to_sign = models.BooleanField(verbose_name="Право подписывать задания", default=False)
    check_edit = models.BooleanField("Возможность редактирования задания", default=True)
    can_make_task = models.BooleanField("Возможность выдавать задания", default=True)
    cpe_flag = models.BooleanField("Флаг ГИП (техническая метка)", default=False)
    mailing_list_check = models.BooleanField("Получать рассылку", default=True)
    work_status = models.BooleanField("Сотрудник работает", default=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        managed = False
        verbose_name = _("сотрудник")
        verbose_name_plural = _("сотрудники")
        db_table = 'ToDo_tasks_employee'


def upload_to(instance, filename):
    name_to_path = str(instance.emp.id)
    new_path = path.join('files',
                         # "media", filename)
                         name_to_path,
                         filename)
    print(new_path)
    return new_path


class MoreDetailsEmployeeModel(models.Model):
    """Дополнительная информация по сотрудникам"""
    emp = models.OneToOneField(EmployeeModel, models.CASCADE, verbose_name="Пользователь")
    photo = models.ImageField(verbose_name="Файл", null=True, blank=True,
                              upload_to=upload_to)
    outside_email = models.EmailField(verbose_name="Внешняя почта", null=True, blank=True)
    mobile_phone = models.CharField(verbose_name="Мобильный телефон", null=True, blank=True, max_length=30)
    date_birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    room = models.CharField(verbose_name="Номер комнаты", null=True, blank=True, max_length=30)
    date_birthday_show = models.BooleanField(verbose_name="Отображать день рождения", default=False, null=True)
    city_dep = models.ForeignKey(CityDepModel, on_delete=models.PROTECT, null=True, verbose_name="Город/Подразделение",
                                 blank=True)
    send_email_salary_blank = models.BooleanField(verbose_name="Отсылать расчетный листок", default=False)
    archive_access = models.BooleanField(verbose_name="Доступ к архиву", default=False)

    class Meta:
        managed = False
        verbose_name = _("дополнительная информация по сотруднику")
        verbose_name_plural = _("дополнительная информация по сотрудникам")
        db_table = 'admin_panel_app_moredetailsemployeemodel'

    def __str__(self):
        return f'{self.emp}'


class CpeModel(models.Model):
    """Таблица ГИП-ов"""
    cpe_user = models.ForeignKey(EmployeeModel, on_delete=models.SET_NULL, verbose_name="Сотрудник", null=True)
    cpe_object = models.ForeignKey(ObjectModel, on_delete=models.PROTECT, verbose_name="Объект", null=True)
    cpe_important = models.BooleanField(verbose_name='Главный за объект', default=False)

    class Meta:
        verbose_name = _("ГИП")
        verbose_name_plural = _("ГИПЫ")
        managed = False
        db_table = 'ToDo_tasks_cpemodel'

    def __str__(self):
        return f'{self.cpe_user}, {self.cpe_object}'


class PrintPagePermissionModel(models.Model):
    """
    Доступ сотрудников к странице печати
    """
    emp = models.ForeignKey(EmployeeModel, verbose_name="Сотрудник", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('сотрудник имеющий доступ к странице печати')
        verbose_name_plural = _('сотрудники имеющие доступ к странице печати')
        managed = False
        db_table = 'page_calculator_app_printpagepermissionmodel'

    def __str__(self):
        return f'{self.emp.last_name} {self.emp.first_name} {self.emp.middle_name}'


# Инвентарные номера
class GeneralInfoInventoryNumberModel(models.Model):
    """Таблица общей информации по инвентарным номерам"""
    order = models.ForeignKey(OrdersModel, verbose_name='Заказчик', on_delete=models.SET_NULL, null=True)
    object_name = models.ForeignKey(ObjectModel, verbose_name='Объект', on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(EmployeeModel, verbose_name='Сотрудник', on_delete=models.SET_NULL, null=True,
                                 related_name='emp_employee')
    date_add = models.DateField(verbose_name='Дата регистрации', auto_now_add=True, null=False)
    return_date = models.DateField(verbose_name='Дата возврата', null=True, blank=True)
    cpe = models.ForeignKey(EmployeeModel, verbose_name='ГИП', on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='cpe_employee')

    class Meta:
        verbose_name = _("общая информация об инвентарном номере")
        verbose_name_plural = _("общая информация об инвентарных номерах")

    def __str__(self):
        return f'{self.id} - {self.order.order}.{self.object_name.object_code}, {self.date_add}'


class OpenInventoryNumbersModel(models.Model):
    """Таблица открытых инвентарных номеров"""
    inventory_number = models.CharField(verbose_name="Открытый инвентарный номер", max_length=8)
    general_info = models.OneToOneField(GeneralInfoInventoryNumberModel, verbose_name='Общая информация',
                                        on_delete=models.CASCADE)
    actual = models.BooleanField(verbose_name='Актуальный', default=True)

    class Meta:
        verbose_name = _('открытый инвентарный номер')
        verbose_name_plural = _('открытие инвентарные номера')

    def __str__(self):
        if self.actual is True:
            actual_str = 'Актуальный'
        else:
            actual_str = 'Аннулирован'
        return f'{self.inventory_number} ({actual_str})'


class CloseInventoryNumbersModel(models.Model):
    """Таблица зыкрытых инвентарных номеров"""
    inventory_number = models.CharField(verbose_name="Закрытый инвентарный номер", max_length=8)
    general_info = models.OneToOneField(GeneralInfoInventoryNumberModel, verbose_name='Общая информация',
                                        on_delete=models.CASCADE)
    actual = models.BooleanField(verbose_name='Актуальный', default=True)

    class Meta:
        verbose_name = _('закрытый инвентарный номер')
        verbose_name_plural = _('закрытые инвентарные номера')

    def __str__(self):
        if self.actual is True:
            actual_str = 'Актуальный'
        else:
            actual_str = 'Аннулирован'
        return f'{self.inventory_number} ({actual_str})'


class KTInventoryNumbersModel(models.Model):
    """Таблица зыкрытых инвентарных номеров"""
    inventory_number = models.CharField(verbose_name="КТ инвентарный номер", max_length=8)
    general_info = models.OneToOneField(GeneralInfoInventoryNumberModel, verbose_name='Общая информация',
                                        on_delete=models.CASCADE)
    actual = models.BooleanField(verbose_name='Актуальный', default=True)

    class Meta:
        verbose_name = _('коммерческий инвентарный номер')
        verbose_name_plural = _('коммерческие инвентарные номера')

    def __str__(self):
        if self.actual is True:
            actual_str = 'Актуальный'
        else:
            actual_str = 'Аннулирован'
        return f'{self.inventory_number} ({actual_str})'


class TypeOfInventoryNumberModel(models.Model):
    name_of_type = models.CharField(verbose_name="Название документации", max_length=100)
    number_of_code_in_ms_access = models.IntegerField(verbose_name='КодТипИнв в MS Access')

    class Meta:
        verbose_name = _('тип инвентарного номера')
        verbose_name_plural = _('типы инвентарных номеров')

    def __str__(self):
        return f'{self.number_of_code_in_ms_access} - {self.name_of_type}'


# Номера разрешений
class GeneralInfoPermissionNumberModel(models.Model):
    """Таблица общей информации по номерам разрешений"""
    order = models.ForeignKey(OrdersModel, verbose_name='Заказчик', on_delete=models.SET_NULL, null=True)
    object_name = models.ForeignKey(ObjectModel, verbose_name='Объект', on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(EmployeeModel, verbose_name='Сотрудник', on_delete=models.SET_NULL, null=True,
                                 related_name='emp_perm_employee')
    date_add = models.DateField(verbose_name='Дата регистрации', auto_now_add=True, null=False)
    return_date = models.DateField(verbose_name='Дата возврата', null=True, blank=True)
    cpe = models.ForeignKey(EmployeeModel, verbose_name='ГИП', on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='cpe_perm_employee')

    class Meta:
        verbose_name = _("общая информация о номере разрешения")
        verbose_name_plural = _("общая информация о номерах разрешений")

    def __str__(self):
        return f'{self.id} - {self.order.order}.{self.object_name.object_code}, {self.date_add}'


class TypeOfPermissionNumberModel(models.Model):
    """Типы разрешений"""
    name_of_type = models.CharField(verbose_name="Название разрешения", max_length=100)
    number_of_code_in_ms_access = models.IntegerField(verbose_name='КодТипДокИзм в MS Access')

    class Meta:
        verbose_name = _('тип номера на разрешение')
        verbose_name_plural = _('типы номеров на разрешения')

    def __str__(self):
        return f'{self.number_of_code_in_ms_access} - {self.name_of_type}'


class PermissionNumbersModel(models.Model):
    """Таблица номеров разрешений для изменения"""
    permission_number = models.CharField(verbose_name="Номер разрешения", max_length=8)
    general_info = models.OneToOneField(GeneralInfoPermissionNumberModel, verbose_name='Общая информация',
                                        on_delete=models.CASCADE)
    actual = models.BooleanField(verbose_name='Актуальный', default=True)

    class Meta:
        verbose_name = _('открытый инвентарный номер')
        verbose_name_plural = _('открытие инвентарные номера')

    def __str__(self):
        if self.actual is True:
            actual_str = 'Актуальный'
        else:
            actual_str = 'Аннулирован'
        return f'{self.permission_number} ({actual_str})'


class ReplacementPermissionNumbersModel(models.Model):
    """Таблица номеров разрешений для изменения"""
    permission_number = models.CharField(verbose_name="Номер разрешения на подмену", max_length=8)
    general_info = models.OneToOneField(GeneralInfoPermissionNumberModel, verbose_name='Общая информация',
                                        on_delete=models.CASCADE)
    actual = models.BooleanField(verbose_name='Актуальный', default=True)

    class Meta:
        verbose_name = _('открытый инвентарный номер')
        verbose_name_plural = _('открытые инвентарные номера')

    def __str__(self):
        if self.actual is True:
            actual_str = 'Актуальный'
        else:
            actual_str = 'Аннулирован'
        return f'{self.permission_number} ({actual_str})'


class ArchiveFilesModel(models.Model):
    """Таблица альбомов """
    album_name = models.CharField(unique=True, verbose_name='Наименование альбома', max_length=128, null=True,
                                  blank=True)
    file_path = models.CharField(verbose_name='Путь к файлу', max_length=2500, null=True, blank=True)
    file_size = models.FloatField(verbose_name='Размер файла', max_length=50, null=True, blank=True)
    md5_file = models.CharField(unique=True, verbose_name='md5 файла', max_length=250, null=True, blank=True)
    data_create = models.DateTimeField(verbose_name='Дата создания', null=True, blank=True)
    date_update = models.DateTimeField(verbose_name='Дата последнего обновления', null=True, blank=True)
    file_was_deleted = models.BooleanField(verbose_name='Файл был удален', default=False)

    class Meta:
        verbose_name = _('архивный файл')
        verbose_name_plural = _('архивные файлы')

    def __str__(self):
        return f'{self.album_name} (md5:{self.md5_file}) {self.file_path}'


class ArchiveEditableFilesModel(models.Model):
    """Таблица альбомов """
    album_name = models.CharField(unique=True, verbose_name='Наименование архива', max_length=128, null=True,
                                  blank=True)
    file_path = models.CharField(verbose_name='Путь к файлу', max_length=2500, null=True, blank=True)
    file_size = models.FloatField(verbose_name='Размер файла', max_length=50, null=True, blank=True)
    md5_file = models.CharField(unique=True, verbose_name='md5 файла', max_length=250, null=True, blank=True)
    data_create = models.DateTimeField(verbose_name='Дата создания', null=True, blank=True)
    date_update = models.DateTimeField(verbose_name='Дата последнего обновления', null=True, blank=True)
    file_was_deleted = models.BooleanField(verbose_name='Файл был удален', default=False)

    class Meta:
        verbose_name = _('файл в редактируемом формате')
        verbose_name_plural = _('файлы в редактируемом формате')

    def __str__(self):
        return f'{self.album_name} (md5:{self.md5_file}) {self.file_path}'


class LogsDownloadsAlbum(models.Model):
    """logs скачивания файлов"""
    download_file_key = models.ForeignKey(ArchiveFilesModel, verbose_name='id скаченного альбома',
                                          on_delete=models.SET_NULL, null=True, blank=True)
    download_file_name = models.CharField(verbose_name='Название скаченного альбома', max_length=300, null=True,
                                          blank=True)
    download_emp_Key = models.ForeignKey(EmployeeModel, verbose_name='id сотрудника скачавшего',
                                         on_delete=models.SET_NULL, max_length=20, null=True, blank=True)
    download_emp_name = models.CharField(verbose_name='Имя сотрудника скачавшего', max_length=300, null=True,
                                         blank=True)
    download_date = models.DateTimeField(verbose_name='Дата и время скачивания', auto_now_add=True, null=False)

    class Meta:
        verbose_name = _('log загрузки')
        verbose_name_plural = _('logs закгрузок')

    def __str__(self):
        return f'{self.download_file_name} - {self.download_emp_name} - {self.download_date}'


class CountsFilesInArchive(models.Model):
    """Счетчик количества файлов в архиве"""

    count_pdf = models.IntegerField(verbose_name='Количество pdf файлов', null=True, blank=True)
    count_editable = models.IntegerField(verbose_name='Количество zip файлов', null=True, blank=True)
    count_of_add_files = models.IntegerField(verbose_name='Количество добавленных файлов', null=True, blank=True)
    date_log = models.DateTimeField(verbose_name='Дата и время обновления', auto_now_add=True, null=False)

    class Meta:
        verbose_name = _('количество файлов')
        verbose_name_plural = _('количество файлов')

    def __str__(self):
        return f'{self.date_log} - {self.count_pdf} - {self.count_editable}'
