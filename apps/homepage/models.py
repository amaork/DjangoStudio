# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ..core.models import Document, get_sequence_choices


class StudioInfo(models.Model):
    """
    工作室基本信息介绍
    """

    # 名称将已超大字体显示在页面顶端
    name = models.CharField('工作室名称', max_length=32)

    # 拼音简写或英文缩写将会显示在页面导航栏左侧
    short_name = models.CharField('拼音简写', max_length=32)

    # 口号将以中号字体显示在工作室名称下方
    slogan = models.CharField('口号', max_length=64)

    # 关于页面介绍信息
    about = models.TextField('工作室简介', max_length=256)
    values = models.TextField('价值理念', max_length=128)

    # 工作室联系方式
    phone = models.CharField('电话', max_length=64, default='')
    wechat = models.CharField('微信', max_length=16,  default='')
    email = models.EmailField('邮箱', max_length=32, default='', blank=True, null=True)
    weibo = models.CharField('微薄', max_length=32, default='', blank=True, null=True)
    address = models.CharField('地址', max_length=128, default='')

    # 图标等媒体文档
    logo = models.ForeignKey(Document, verbose_name='公司 LOGO', related_name='logo')
    icon = models.ForeignKey(Document, verbose_name='浏览器 ICO', related_name='ico')
    qr_code = models.ForeignKey(Document, verbose_name='微信二维码', related_name='wechat')


class Service(models.Model):
    """
    工作室服务项目介绍
    """
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

    def __str__(self):
        return '{0:s}:{1:s}'.format(self.sequence, self.name)


class Message(models.Model):
    """
    客户留言信息
    """
    name = models.CharField('昵称', max_length=16)
    comment = models.TextField('留言内容', max_length=128)
    contact = models.CharField('电话或微信', max_length=16)

    @staticmethod
    def add_user_message(name, contact, comment):
        """
        接收来自网页,联系我们的留言信息
        :param name: 客户名称
        :param contact: 客户联系方式
        :param comment: 客户留言内容
        :return:
        """
        Message.objects.create(name=name, contact=contact, comment=comment)


class Custom(models.Model):
    """
    客户信息
    """

    # TODO: 改善显示效果
    name = models.CharField('昵称', max_length=16)
    work = models.CharField('职业', max_length=16, default='', blank=True, null=True)
    city = models.CharField('地址', max_length=16, default='', blank=True, null=True)
    comment = models.TextField('评价', max_length=256)
    avatar = models.ForeignKey(Document, verbose_name="头像", related_name='avatar', blank=True, null=True)

    # display = Tre, 将会在首页客户评价中显示
    display = models.BooleanField('首页展示', default=False)


class PaymentPlan(models.Model):
    MAX_ITEM = 3
    SEQ_CHOICES = get_sequence_choices(MAX_ITEM)

    name = models.CharField('名称', max_length=16)

    # 价格控制
    origin_price = models.IntegerField('原价', blank=True, null=True)
    current_price = models.IntegerField('现价')
    discount = models.FloatField('折扣', blank=True, null=True,
                                 default=1.0, validators=[MinValueValidator(0.1), MaxValueValidator(1.0)])

    desc = models.TextField('付费简述', max_length=64, blank=True, null=True)
    detail = models.TextField('详细介绍', max_length=512, blank=True, null=True)
    sequence = models.CharField('顺序', max_length=1, choices=SEQ_CHOICES)
