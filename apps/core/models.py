# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.db import models
import string
import os


__all__ = ['Document', 'get_sequence_choices']


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
