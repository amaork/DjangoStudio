# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from .models import Navigation


def redirect_to_anchor(request, parent, anchor):
    for navigation in Navigation.objects.filter(is_anchor=True):
        if parent == navigation.parent and anchor == navigation.url:
            return HttpResponseRedirect("/{0:s}/#{1:s}".format(parent, anchor))
    else:
        return Http404('Do not found pages')
