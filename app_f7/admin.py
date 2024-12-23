from django.contrib import admin
from .models import  *

class Departments_Admin(admin.ModelAdmin):
    list_display = ('id', 'department', 'profile', 'sort')


class Move_Admin(admin.ModelAdmin):


    # все видят все обращения
    """
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Request.objects.all()
        else:
            return Request.objects.filter(Add=request.user)
    """

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'Add', None) is None:
            obj.Add = request.user
        obj.save()

    list_display = ('id','date', 'department', 'type_rean', 'type_pay', 'goin', 'count_finish')
    #search_fields = ['request_date', 'patient_f', 'request_f']

    list_per_page = 40
    view_on_site = True
    #date_hierarchy = 'request_date'
    list_display_links = ('department', 'type_rean', 'type_pay')


admin.site.register(t_move, Move_Admin)
admin.site.register(s_department, Departments_Admin)
admin.site.register(s_type_rean)
admin.site.register(s_profile)
admin.site.register(s_type_pay)

