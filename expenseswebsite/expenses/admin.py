from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Expense, Lineas, TipoSocio, Genero, Comite, Estado, EstadoCivil, Aseguradora, Recaudador, Pago, Nacionalidad, Clase
# Register your models here.

class ExpenseResource(resources.ModelResource):
    class Meta:
        model = Expense
class ExpenseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ExpenseResource

admin.site.register(Expense, ImportExportModelAdmin)
admin.site.register(Lineas)
admin.site.register(TipoSocio)
admin.site.register(Genero)
admin.site.register(Comite)
admin.site.register(EstadoCivil)
admin.site.register(Estado)
admin.site.register(Aseguradora)
admin.site.register(Recaudador)
admin.site.register(Pago)
admin.site.register(Nacionalidad)
admin.site.register(Clase)