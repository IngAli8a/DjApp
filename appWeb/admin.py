from django.contrib import admin
from .models import InfoMed, demanda_diarias, admin_indi, AdminMed, StockMed, SaldoAnterior, indi_mensuales

# Register your models here.
admin.site.register(InfoMed)
admin.site.register(demanda_diarias)
admin.site.register(admin_indi)
admin.site.register(AdminMed)
admin.site.register(StockMed)
admin.site.register(SaldoAnterior)
admin.site.register(indi_mensuales)