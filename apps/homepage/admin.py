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


class PaymentItemInline(admin.StackedInline):
    model = PaymentItem
    extra = PaymentItem.MAX_ITEM

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= PaymentItem.MAX_ITEM:
            return False
        else:
            return True


class PaymentItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin_price', 'current_price', 'plan')


class PaymentPlayAdmin(LimitInstanceAdmin):
    list_display = ('name', 'desc', 'size')
    inlines = [PaymentItemInline]


admin.site.register(Custom)
admin.site.register(Message, MessageAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(StudioInfo, StudioInfoAdmin)

admin.site.register(PaymentItem, PaymentItemAdmin)
admin.site.register(PaymentPlan, PaymentPlayAdmin)

