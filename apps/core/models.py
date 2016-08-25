# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.db import models
import string
import os


__all__ = ['Document', 'Message', 'Picture', 'Gallery', 'Navigation', 'NavigationModel', 'get_sequence_choices']


def get_sequence_choices(size):
    """
    根据 size 生成顺序选择元组
    :param size:
    :return:
    """
    if size > len(string.digits):
        size = len(string.digits)

    return zip(str(string.digits[:size]), range(size))


class Document(models.Model):
    """
    文件 Model 负责上传存储各种类型的文件数据
    """
    PATH_FORMAT = "documents/%Y/%m/%d"

    name = models.CharField(max_length=32, unique=True)
    file = models.FileField(upload_to=PATH_FORMAT)

    def __str__(self):
        return self.name

    def url(self):
        return self.file.url

    def file_path(self):
        return self.file.name

    @staticmethod
    def get_upload_path():
        return timezone.now().strftime(Document.PATH_FORMAT)


@receiver(pre_delete, sender=Document)
def delete_document(sender, instance, **kwargs):
    if not isinstance(instance, Document):
        return

    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


@receiver(pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not isinstance(instance, Document):
        return False

    if not instance.pk:
        return False

    try:

        new = instance.file
        old = Document.objects.get(pk=instance.pk).file

        # New file and old file is not same one
        if (not (old == new)) and os.path.isfile(old.path):
            os.remove(old.path)
    except Document.DoesNotExist:
        return False


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


class Gallery(models.Model):
    MAX_ITEM = 99

    name = models.CharField('名称', max_length=32)
    desc = models.TextField('描述', max_length=128, blank=True, null=True)
    cover = models.ForeignKey(Document, verbose_name='相册封面', related_name='cover')

    def size(self):
        """
        获取相册图像个数
        :return:
        """
        return len(self.get_pictures())

    def get_pictures(self):
        """
        获取相册图像列表
        :return:
        """
        return Picture.objects.filter(gallery=self)

    size.short_description = '图像个数'


class Picture(models.Model):
    desc = models.CharField('图片描述', max_length=64, blank=True, null=True)
    picture = models.ForeignKey(Document, verbose_name='图像文件')
    gallery = models.ForeignKey(Gallery, verbose_name='相册')


class Navigation(models.Model):
    """
    导航栏
    """
    MAX_ITEM = 10
    SEQ_CHOICES = get_sequence_choices(MAX_ITEM)

    text = models.CharField("名称", max_length=16, unique=True)
    url = models.CharField("链接", max_length=64, unique=True)
    sequence = models.CharField('顺序', max_length=1, choices=SEQ_CHOICES)

    def __str__(self):
        return self.text

    @staticmethod
    def get_anchor_context():
        context = dict()
        context['type'] = '#'
        context['items'] = Navigation.objects.all().order_by('sequence')
        return context

    @staticmethod
    def get_hyperlink_context():
        context = dict()
        context['type'] = '/'
        context['items'] = Navigation.objects.all().order_by('sequence')
        return context


class NavigationModel(models.Model):
    """
    继承 NavigationModel 后，定义 url, text, sequence 在保存模块的时候将会自动创建 NavigationBar Instance
    """
    url = ""
    text = ""
    sequence = -1

    @staticmethod
    def get_top_sequence():
        return 0

    @staticmethod
    def get_bottom_sequence():
        return Navigation.MAX_ITEM - 1

    def save(self, *args, **kwargs):
        if len(self.text) and len(self.url) and self.sequence != -1:
            if not Navigation.objects.filter(url=self.url, text=self.text):
                Navigation.objects.create(text=self.text, url=self.url, sequence=self.sequence)
        super(NavigationModel, self).save(*args, **kwargs)
