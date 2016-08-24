from django.contrib import admin
from .models import *
from ..core.admin import LimitInstanceAdmin


class ServiceAdmin(LimitInstanceAdmin):
    limit = Service.MAX_ITEM
    list_display = ['name', 'sequence']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'comment')


class StudioInfoAdmin(LimitInstanceAdmin):
    list_display = ('name', 'short_name', 'slogan')


class PaymentPlayAdmin(LimitInstanceAdmin):
    limit = PaymentPlan.MAX_ITEM
    list_display = ('name', 'origin_price', 'current_price', 'discount', 'desc')


admin.site.register(Custom)
admin.site.register(Message, MessageAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(StudioInfo, StudioInfoAdmin)
admin.site.register(PaymentPlan, PaymentPlayAdmin)

