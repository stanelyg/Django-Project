from django.contrib import admin
from django.contrib.auth.models import Permission
from  dbmaster.models import WorkingHour,SalaryYear,SalaryPeriod
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(Permission)

@admin.register(WorkingHour)
class WorkingHour(ImportExportModelAdmin) :
    pass

class SalaryPeriodInline(admin.TabularInline):
      model=SalaryPeriod
@admin.register(SalaryYear)
class SalaryPeriodAdmin(admin.ModelAdmin):
      inlines=[SalaryPeriodInline]