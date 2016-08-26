# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages


from ..core.models import Gallery, Navigation, Message
from ..core.forms import UserMessageForm
from .models import *


def homepage(request):
    if request.method == 'POST':
        form = UserMessageForm(request.POST)
        if form.is_valid():
            # 保存用户留言信息
            name = request.POST.get('name')
            contact = request.POST.get('contact')
            comment = request.POST.get('comment')
            Message.add_user_message(name, contact, comment)

            # 发送成功信息到 contact_us 页面
            messages.add_message(request, messages.INFO, '谢谢,我们会尽快联系您!')
            return HttpResponseRedirect('/homepage/#success')
        else:
            # 发送失败信息到 contact_us 页面
            # TODO: 返回的信息中包含用户未完成的表单
            messages.add_message(request, messages.WARNING, '请完整填写留言信息!')
            return HttpResponseRedirect('/homepage/#warning')
    else:
        form = UserMessageForm()

    context = {
        'form': form,
        'studio': get_object_or_404(StudioInfo),
        'contact': get_object_or_404(ContactInfo),
        'customs': CustomComment.objects.all(),
        'payments': StudioInfo.get_context_data(),
        'services': Service.get_context_data(),
        'navigation': Navigation.get_anchor_context(),
    }
    return render(request, 'homepage/index.html', context)


def gallery(request, pk):
    studio = get_object_or_404(StudioInfo)
    gallery = get_object_or_404(Gallery, pk=pk)

    context = {

        'studio': studio,
        'title': gallery.name,
        'pictures': gallery.get_pictures(),
        'navigation': Navigation.get_hyperlink_context(),
    }
    return render(request, 'homepage/gallery.html', context)


def service(request, pk):
    studio = get_object_or_404(StudioInfo)
    instance = get_object_or_404(Service, pk=pk)

    context = {

        'studio': studio,
        'return': '/homepage/anchor/services',
        'service': instance,
        'navigation': Navigation.get_hyperlink_context(),
    }
    return render(request, 'homepage/service.html', context)
