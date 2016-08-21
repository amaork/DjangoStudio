from django.contrib import admin
from .models import *
from ..core.admin import LimitInstanceAdmin


class ServiceAdmin(LimitInstanceAdmin):
    limit = Service.MAX_ITEM
    list_display = ['name', 'sequence']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'comment')


admin.site.register(Custom)
admin.site.register(StudioInfo)
admin.site.register(PaymentPlan)
admin.site.register(Message, MessageAdmin)
admin.site.register(Service, ServiceAdmin)

