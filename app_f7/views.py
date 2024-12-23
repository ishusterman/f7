from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import *
import datetime
from django.db.models import Max
from django.contrib.auth import logout
from django.shortcuts import redirect
from .form import *
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from datetime import datetime, date, time, timedelta

from django.db.models import Count, Avg, Sum

from .report import *

def logoff(request):
    logout(request)
    return redirect('/index/')

def date_convert_to_usa(date):
    date = date.split(".")
    res=date[2]+"-"+(date[1])+"-"+date[0]
    return res

# выборка для первых итогов
def get_foot1(type_pay_item,date):
    res=[]
    for profile in s_profile.objects.all():
        for type_rean in s_type_rean.objects.all():
            rec =[]
            rec.append(profile)
            rec.append(type_rean)

            qs = t_move.objects.filter(type_pay=type_pay_item).filter(date=date).filter(type_rean=type_rean).filter(
                department__profile=profile)

            num = qs.aggregate(Sum('count'))
            rec.append(num.get('count__sum'))
            num = qs.aggregate(Sum('goin'))
            rec.append(num.get('goin__sum'))

            num = qs.aggregate(Sum('go_in_from_ds'))
            rec.append(num.get('go_in_from_ds__sum'))
            num = qs.aggregate(Sum('go_in_from_selo'))
            rec.append(num.get('go_in_from_selo__sum'))

            num = qs.aggregate(Sum('go_in_to_17'))
            rec.append(num.get('go_in_to_17__sum'))
            num = qs.aggregate(Sum('go_in_up_60'))
            rec.append(num.get('go_in_up_60__sum'))

            num = qs.aggregate(Sum('go_in_from_other_stac'))
            rec.append(num.get('go_in_from_other_stac__sum'))
            num = qs.aggregate(Sum('go_in_to_other_stac'))
            rec.append(num.get('go_in_to_other_stac__sum'))

            num = qs.aggregate(Sum('go_out'))
            rec.append(num.get('go_out__sum'))
            num = qs.aggregate(Sum('go_out_to_other_stac'))
            rec.append(num.get('go_out_to_other_stac__sum'))

            num = qs.aggregate(Sum('go_out_to_ds'))
            rec.append(num.get('go_out_to_ds__sum'))
            num = qs.aggregate(Sum('death'))
            rec.append(num.get('death__sum'))

            num = qs.aggregate(Sum('count_finish'))
            rec.append(num.get('count_finish__sum'))
            num = qs.aggregate(Sum('count_finish_selo'))
            rec.append(num.get('count_finish_selo__sum'))

            num = qs.aggregate(Sum('count_finish_mother'))
            rec.append(num.get('count_finish_mother__sum'))

            res.append(rec)
    return res


# выборка для первых итогов
def get_foot2(type_pay_item,date):
    res=[]

    for type_rean in s_type_rean.objects.all():
            rec =[]
            rec.append("     ")
            rec.append(type_rean)

            qs = t_move.objects.filter(type_pay=type_pay_item).filter(date=date).filter(type_rean=type_rean)

            num = qs.aggregate(Sum('count'))
            rec.append(num.get('count__sum'))
            num = qs.aggregate(Sum('goin'))
            rec.append(num.get('goin__sum'))

            num = qs.aggregate(Sum('go_in_from_ds'))
            rec.append(num.get('go_in_from_ds__sum'))
            num = qs.aggregate(Sum('go_in_from_selo'))
            rec.append(num.get('go_in_from_selo__sum'))

            num = qs.aggregate(Sum('go_in_to_17'))
            rec.append(num.get('go_in_to_17__sum'))
            num = qs.aggregate(Sum('go_in_up_60'))
            rec.append(num.get('go_in_up_60__sum'))

            num = qs.aggregate(Sum('go_in_from_other_stac'))
            rec.append(num.get('go_in_from_other_stac__sum'))
            num = qs.aggregate(Sum('go_in_to_other_stac'))
            rec.append(num.get('go_in_to_other_stac__sum'))

            num = qs.aggregate(Sum('go_out'))
            rec.append(num.get('go_out__sum'))
            num = qs.aggregate(Sum('go_out_to_other_stac'))
            rec.append(num.get('go_out_to_other_stac__sum'))

            num = qs.aggregate(Sum('go_out_to_ds'))
            rec.append(num.get('go_out_to_ds__sum'))
            num = qs.aggregate(Sum('death'))
            rec.append(num.get('death__sum'))

            num = qs.aggregate(Sum('count_finish'))
            rec.append(num.get('count_finish__sum'))
            num = qs.aggregate(Sum('count_finish_selo'))
            rec.append(num.get('count_finish_selo__sum'))

            num = qs.aggregate(Sum('count_finish_mother'))
            rec.append(num.get('count_finish_mother__sum'))

            res.append(rec)
    return res



# проверям есть ли все необходимые строки на данную дату и вид оплаты
def need_correct(type_pay_item,date):
    queryset = t_move.objects.filter(type_pay=type_pay_item).filter(date=date)
    if (queryset.count() == (s_type_rean.objects.all().count()*s_department.objects.all().count())):
        return False
    else:
        return True

# добавляем строки при необходимости
def correct(type_pay, date):
    queryset = t_move.objects.all()
    pay = s_type_pay.objects.filter(id=type_pay).first()
    for department in s_department.objects.all():
        for type_rean in s_type_rean.objects.all():
            if queryset.filter(department=department).filter(type_rean=type_rean).filter(date=date).filter(type_pay=pay).count() == 0:
                rec = t_move(department=department, type_rean=type_rean, date=date, type_pay=pay)
                rec.save()


    return True

# вычисляем итог дня
def calc_count_finish(date, type_pay):
    #queryset = t_move.objects.all()
    #qs = queryset.filter(date=date_convert_to_usa(date))
    qs = t_move.objects.filter(date=date_convert_to_usa(date), type_pay=type_pay)

    for item in qs: # проход по текущему дню
            id = item.id
            curr_item = t_move.objects.get(id=id)
            count_finish=curr_item.count+ curr_item.goin +curr_item.go_in_from_other_stac-curr_item.go_in_to_other_stac - curr_item.go_out - curr_item.death

            #rec = t_move.objects.get(id=id)
            if count_finish >= 0:
                curr_item.count_finish = count_finish
            else:
                curr_item.count_finish = 0

            curr_item.save()

    return True


# переносим остатки с прошлого дня
def move(date,type_pay_item):
    queryset = t_move.objects.all()
    # накануне
    yd = datetime.strptime(date,'%d.%m.%Y')-timedelta(days=1)
    qs_yd =  queryset.filter(date=yd).filter(type_pay=type_pay_item)

    # сегодня
    qs = queryset.filter(date=date_convert_to_usa(date)).filter(type_pay=type_pay_item)

    if qs_yd.count()>0: # если есть предыдущий день
        for item in qs: # проход по текущему дню
            id = item.id
            department=item.department
            type_rean=item.type_rean
            type_pay= item.type_pay

            id_yd = t_move.objects.get(date=yd, department=department, type_pay=type_pay, type_rean=type_rean).id
            count_finish=t_move.objects.get(id=id_yd).count_finish

            rec = t_move.objects.get(id=id)
            rec.count = count_finish
            rec.save()

    return True

@login_required(login_url='/login/')
def report(request):

    if 'report1' in request.POST:
        return create_report1(request)

    if 'report2' in request.POST:
        return create_report2(request)

    if 'report3' in request.POST:
        return create_report3(request)

    if 'report4' in request.POST:
        return create_report4(request)


    type_pay = s_type_pay.objects.all()
    department= s_department.objects.all()
    now = datetime.today()
    date2 = date1 = str(now.day) + "." + str(now.month) + "." + str(now.year)

    context = {'type_pay': type_pay, 'department': department, 'date1': date1,'date2': date2}
    return render(request, 'report.html', context)


@login_required(login_url='/login/')
def index(request):
    t_move_formset = modelformset_factory(t_move, fields='__all__', extra=0)
    type_pay_item = 1

    now = datetime.today()
    date = str(now.day) + "." + str(now.month) + "." + str(now.year)
    res = date_convert_to_usa(date)

    """
    if 'move' in request.POST:
        type_pay_item = request.POST['type_pay_item']
        date = (request.POST['date'])
        res = date_convert_to_usa(date)
        move(date, type_pay_item)
    """

    if 'filter' in request.POST:
        type_pay_item = request.POST['type_pay']
        date = (request.POST['date'])
        res = date_convert_to_usa(date)
        if need_correct(type_pay_item,res):
            correct(type_pay_item, res)


    if 'save' in request.POST:
        type_pay_item = request.POST['type_pay_item']
        date = (request.POST['date'])
        res = date_convert_to_usa(date)

        formset = t_move_formset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)

        calc_count_finish(date, type_pay_item)


    if need_correct(type_pay_item, res):
        correct(type_pay_item, res)
    move(date,type_pay_item)

    queryset = t_move.objects.filter(type_pay=type_pay_item).filter(date=res).order_by("department__sort","type_rean__id")
    formset = t_move_formset(queryset=queryset)

    
    foot1 = get_foot1(type_pay_item, res)
    foot2 = get_foot2(type_pay_item, res)
    #foot1 = []
    #foot2 = []

    type_pay = s_type_pay.objects.all()
    department = s_department.objects.all()
    type_rean = s_type_rean.objects.all()
    
    context = {'formset': formset, 'type_pay': type_pay, 'type_pay_item': int(type_pay_item),'date': date, 'foot1' : foot1, 'foot2' : foot2,
               'department': department, 'type_rean': type_rean}


    return render(request, 'index.html', context)


