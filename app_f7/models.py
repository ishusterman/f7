from django.db import models
from datetime import date
from django.contrib.auth.models import User

class s_profile(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.CharField(verbose_name="Профиль", max_length=50, blank=True)

    def __str__(self):
        return self.profile

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class s_department(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(verbose_name="Отделение", max_length=50, blank=True)
    profile = models.ForeignKey(s_profile, verbose_name="Профиль", default=None,
                                blank=True, null=True, on_delete=models.DO_NOTHING)
    sort = models.PositiveIntegerField(verbose_name="Порядок сортировки", blank=False)

    def __str__(self):
        return self.department

    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'

class s_type_rean(models.Model):
    id = models.AutoField(primary_key=True)
    type_rean = models.CharField(verbose_name="Вид реанимации", max_length=50, blank=True)

    def __str__(self):
        return self.type_rean

    class Meta:
        verbose_name = 'Вид реанимации'
        verbose_name_plural = 'Виды реанимации'

class s_type_pay(models.Model):
    id = models.AutoField(primary_key=True)
    type_pay = models.CharField(verbose_name="Вид оплаты", max_length=50, blank=True)

    def __str__(self):
        return self.type_pay

    class Meta:
        verbose_name = 'Вид оплаты'
        verbose_name_plural = 'Виды оплаты'



class t_move(models.Model):

    id = models.AutoField(primary_key=True)

    department = models.ForeignKey(s_department, verbose_name="Отделение", default=None,
                                 blank=True, null=True, on_delete=models.DO_NOTHING)

    type_rean = models.ForeignKey(s_type_rean, verbose_name="Вид реанимации", default=None,
                                     blank=True, null=True, on_delete=models.DO_NOTHING)

    type_pay = models.ForeignKey(s_type_pay, verbose_name="Вид оплаты", default=None,
                                  blank=True, null=True, on_delete=models.DO_NOTHING)



    date = models.DateField(verbose_name="Дата", default=date.today)

    count = models.PositiveIntegerField(verbose_name="Состоит", blank=False, default="0")
    goin = models.PositiveIntegerField(verbose_name="Поступило всего", blank=False, default="0")
    go_in_from_ds = models.PositiveIntegerField(verbose_name="Пост их ДС", blank=False , default="0")
    go_in_from_selo = models.PositiveIntegerField(verbose_name="Пост из села", blank=False, default="0")
    go_in_to_17 = models.PositiveIntegerField(verbose_name="Детей до 17 лет", blank=False, default="0")
    go_in_up_60 = models.PositiveIntegerField(verbose_name="Старше 60 лет", blank=False, default="0")
    go_in_from_other_stac = models.PositiveIntegerField(verbose_name="Переведено из др. отделения", blank=False, default="0")
    go_in_to_other_stac = models.PositiveIntegerField(verbose_name="Переведено в др. отделение", blank=False, default="0")
    go_out = models.PositiveIntegerField(verbose_name="Выписано всего", blank=False, default="0")

    go_out_to_other_stac = models.PositiveIntegerField(verbose_name="Выписано в др. стационар", blank=False, default="0")

    go_out_to_ds = models.PositiveIntegerField(verbose_name="Выписано в ДС", blank=False, default="0")
    death = models.PositiveIntegerField(verbose_name="Умерло", blank=False, default="0")
    count_finish = models.PositiveIntegerField(verbose_name="Состоит всего", blank=False, default="0")
    count_finish_selo = models.PositiveIntegerField(verbose_name="Состоит сельских жителей", blank=False, default="0")
    count_finish_mother = models.PositiveIntegerField(verbose_name="Состоит матерей", blank=False, default="0")



    Add = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.department)

    class Meta:
        verbose_name = 'Движение'
        verbose_name_plural = 'Движения'

    def __unicode__(self):
        return self.id


