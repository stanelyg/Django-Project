from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (Nhif, NhifDetail, Nssfreferencetable,
                     PayeRelief, Payetable,OverTimeSetting)


@admin.register(OverTimeSetting)

class OverTimeSettingAdmin(admin.ModelAdmin):
      pass

class PayeTableInline(admin.TabularInline):
      model=Payetable

@admin.register(PayeRelief)

class PayeReliefAdmin(admin.ModelAdmin):
     inlines=[PayeTableInline]


@admin.register(Nssfreferencetable)
class Nssfreferencetable(ImportExportModelAdmin) :
    pass
#For Imports

@admin.register(NhifDetail)
class NhifDetail(ImportExportModelAdmin) :
    pass

# class NhifDetailInline(admin.TabularInline):
#       model = NhifDetail

@admin.register(Nhif)
class Nhif(ImportExportModelAdmin) :
    pass
    #   inlines = [
    #         NhifDetailInline,
    #   ]

