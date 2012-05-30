# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import time

from zope.component import getMultiAdapter
from zope.security.interfaces import IPrincipal
from uvc.adhoc.interfaces import IAdHocUserInfo
from zope.publisher.interfaces.http import IHTTPRequest


class DateFolder(grok.Container):

    def getContentType(self):
        return 

    def getContentName(self):
        return "RUMS"

    def add(self, content):
        self[content.principal.id] = content


def getAdHocUserInfo(principal, request):
    return getMultiAdapter((principal, request), IAdHocUserInfo)


class AdHocUserInfo(grok.MultiAdapter):
    grok.adapts(IPrincipal, IHTTPRequest)
    grok.implements(IAdHocUserInfo)
    grok.baseclass()

    def __init__(self, principal, request):
        self.principal = principal
        self.request = request

    @property
    def formular_informationen(self):
        raise NotImplementedError

    def getDateFolder(self):
        base = grok.getSite()['dokumente']
        folder_name = time.strftime('%Y_%m_%d', time.localtime())
        if not folder_name in base.keys():
            base[folder_name] = DateFolder()
        return base[folder_name]

    def getAddLink(self):
        datefolder = self.getDateFolder()
        addlink = "@@%s" % self.formular_informationen.get('titel').replace(' ', '_').lower()
        return grok.url(self.request, datefolder, addlink)
