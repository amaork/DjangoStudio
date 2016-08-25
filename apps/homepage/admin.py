from django.contrib import admin
from .models import *
from ..core.admin import LimitInstanceAdmin, LimitInlineInstanceAdmin, OrderedModelAdmin


class ServiceAdmin(OrderedModelAdmin):
    limit = Service.MAX_ITEM
    list_display = ['name', 'sequence']


class StudioInfoAdmin(LimitInstanceAdmin):
    list_display = ('name', 'short_name', 'slogan')


class ContactInfoAdmin(LimitInstanceAdmin):
    list_display = ('phone', 'wechat', 'address')


class PaymentItemInline(LimitInlineInstanceAdmin):
    model = PaymentItem
    extra = PaymentItem.MAX_ITEM
    limit = PaymentPlan.MAX_ITEM


class PaymentItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin_price', 'current_price', 'plan')


class PaymentPlanAdmin(LimitInstanceAdmin):
    list_display = ('name', 'desc', 'size')
    inlines = [PaymentItemInline]


class CustomCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'primary')


admin.site.register(StudioInfo, StudioInfoAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)

admin.site.register(PaymentItem, PaymentItemAdmin)
admin.site.register(PaymentPlan, PaymentPlanAdmin)

admin.site.register(Service, ServiceAdmin)
admin.site.register(CustomComment, CustomCommentAdmin)
