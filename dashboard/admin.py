from django.contrib import admin
from dashboard.d_models import StoreProfile,ReportProfile

# Register your models here.

class StoreProfileAdmin(admin.ModelAdmin):
    list_display = ("storename","slug")
    prepopulated_fields = {"slug" : ("storename",)}
admin.site.register(StoreProfile,StoreProfileAdmin)

admin.site.register(ReportProfile)