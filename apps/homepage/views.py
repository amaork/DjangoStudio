# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import StudioInfo, Custom, Service, PaymentPlan, Message
from .forms import UserMessageForm


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

    studio = get_object_or_404(StudioInfo)

    context = {
        'form': form,
        'studio': studio,
        'customs': Custom.objects.filter(display=True),
        'payments': PaymentPlan.objects.all().order_by('sequence'),
        'services': [Service.get_group_item(x) for x in range(Service.get_group_size())],
    }
    return render(request, 'homepage/index.html', context)

