# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.db import models
from ..core.models import Document, NavigationModel, get_sequence_choices


class StudioInfo(NavigationModel):
    """
    工作室基本信息介绍
    """
    url = 'about'
    text = '关于'
    sequence = NavigationModel.get_top_sequence()

    # 名称将已超大字体显示在页面顶端
    name = models.CharField('工作室名称', max_length=32)

    # 拼音简写或英文缩写将会显示在页面导航栏左侧
    short_name = models.CharField('拼音简写', max_length=32)

    # 口号将以中号字体显示在工作室名称下方
    slogan = models.CharField('口号', max_length=64)

    # 主推付费计划
    primary_payment_plan = models.ForeignKey('PaymentPlan', verbose_name='主推付费计划', blank=True, null=True)

    # 关于页面介绍信息
    about = models.TextField('工作室简介', max_length=512)
    values = models.TextField('价值理念', max_length=512)

    # 图标等媒体文档
    logo = models.ForeignKey(Document, verbose_name='公司 LOGO', related_name='logo')
    icon = models.ForeignKey(Document, verbose_name='浏览器 ICO', related_name='ico')

    @staticmethod
    def get_primary_payment_plan():
        studio = get_object_or_404(StudioInfo)
        if not isinstance(studio, StudioInfo):
            return None

        plan = studio.primary_payment_plan
        if not isinstance(plan, PaymentPlan):
            return None

        context = dict()
        context['name'] = plan.name
        context['desc'] = plan.desc
        context['plan'] = plan.get_plans()
        return context


class ContactInfo(NavigationModel):
    """
    工作室联系方式
    """
    url = 'contact'
    text = '联系我们'
    sequence = NavigationModel.get_bottom_sequence()

    phone = models.CharField('电话', max_length=64, default='')
    wechat = models.CharField('微信', max_length=16,  default='')
    address = models.CharField('地址', max_length=128, default='')
    email = models.EmailField('邮箱', max_length=32, default='', blank=True, null=True)
    weibo = models.CharField('微薄', max_length=32, default='', blank=True, null=True)
    qr_code = models.ForeignKey(Document, verbose_name='微信二维码', related_name='wechat')


class Service(NavigationModel):
    """
    工作室服务项目介绍
    """
    url = 'services'
    text = '服务项目'
    sequence = NavigationModel.get_top_sequence() + 1

    MAX_ITEM = 9
    GROUP_ITEM = 3
    SEQ_CHOICES = get_sequence_choices(MAX_ITEM)

    name = models.CharField('服务名称', max_length=16, unique=True)

    # 服务简述,放在名称图像下方
    desc = models.TextField('服务简述', max_length=128)

    # 服务的详细信息, 点开之后可以查看
    # TODO: 考虑使用 Collapse,或链接实现
    detail = models.TextField('详细介绍', max_length=512, blank=True, null=True)

    # 服务的顺序, 1 - 9 三个一组排列成一排
    sequence = models.CharField('顺序', max_length=1, choices=SEQ_CHOICES)

    # 服务的显示图标
    icon = models.ForeignKey(Document, verbose_name='服务图标')

    @staticmethod
    def get_group_size():
        return int(Service.MAX_ITEM / Service.GROUP_ITEM)

    @staticmethod
    def get_group_item(group):
        return Service.objects.all().order_by('sequence')[group * Service.GROUP_ITEM: (group + 1) * Service.GROUP_ITEM]

    @staticmethod
    def get_context_data():
        return [Service.get_group_item(x) for x in range(Service.get_group_size())]

    def __str__(self):
        return '{0:s}:{1:s}'.format(self.sequence, self.name)


class CustomComment(NavigationModel):
    """
    客户评价
    """
    url = 'portfolio'
    text = '客户评价'
    sequence = NavigationModel.get_top_sequence() + 2

    name = models.CharField('昵称', max_length=16)
    work = models.CharField('职业', max_length=16, default='', blank=True, null=True)
    city = models.CharField('地址', max_length=16, default='', blank=True, null=True)
    comment = models.TextField('评价', max_length=256)
    avatar = models.ForeignKey(Document, verbose_name='头像', related_name='avatar', blank=True, null=True)

    # display = Tre, 将会在首页客户评价中显示
    primary = models.BooleanField('首页展示', default=False)


class PaymentPlan(NavigationModel):
    """
    付费计划，一个付费计划下可以有多个付费项目
    """
    url = 'pricing'
    text = '付费项目'
    sequence = NavigationModel.get_top_sequence() + 3

    MAX_ITEM = 3
    name = models.CharField('付费计划名称', max_length=16)
    desc = models.CharField('付费计划介绍', max_length=128)

    def __str__(self):
        return self.name

    def size(self):
        """
        获取付费项目个数
        :return:
        """
        return len(self.get_plans())

    def get_plans(self):
        """
        获取付费项目
        :return:
        """
        return PaymentItem.objects.filter(plan=self).order_by('sequence')

    def save(self, *args, **kwargs):
        self.text = self.name
        super(PaymentPlan, self).save(*args, **kwargs)

    size.short_description = '个数'


class PaymentItem(models.Model):
    """
    付费项目
    """
    MAX_ITEM = 3
    SEQ_CHOICES = get_sequence_choices(MAX_ITEM)

    name = models.CharField('名称', max_length=16)
    origin_price = models.IntegerField('原价', blank=True, null=True)
    current_price = models.IntegerField('现价')
    desc = models.TextField('简述', max_length=64, blank=True, null=True)
    detail = models.TextField('详细介绍', max_length=512, blank=True, null=True)
    plan = models.ForeignKey(PaymentPlan, verbose_name='付费计划')
    sequence = models.CharField('显示顺序', max_length=1, choices=SEQ_CHOICES)

