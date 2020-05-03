from django.contrib import admin
from .models import CurrencyTransferHistory

class CurrencyTransferHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CurrencyTransferHistory._meta.get_fields()]
admin.site.register(CurrencyTransferHistory,CurrencyTransferHistoryAdmin)



