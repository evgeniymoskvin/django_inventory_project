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



