# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import time

from zope.component import getUtility
from zope.component import getMultiAdapter
from uvc.adhoc.interfaces import IAdHocUserInfo
from zope.security.interfaces import IPrincipal
from zope.publisher.interfaces.http import IHTTPRequest
from uvc.adhoc import AdHocProductFolder, IAdHocIdReference


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

    def getProductFolder(self):
        base = grok.getSite()['dokumente']
        folder_name = time.strftime('%Y_%m_%d', time.localtime())
        if not folder_name in base.keys():
            base[folder_name] = AdHocProductFolder()
        return base[folder_name]

    def getAddLink(self):
        obj = self.getObject()
        if obj:
            return grok.url(self.request, obj)
        datefolder = self.getProductFolder()
        addlink = "@@%s" % (
            self.formular_informationen.get('titel').replace(' ', '_').lower())
        return grok.url(self.request, datefolder, addlink)

    def getObject(self):
        util = getUtility(IAdHocIdReference)
        if not self.principal.id.isdigit():
            return
        return util.queryObject(int(self.principal.id))

    @property
    def clearname(self):
        if not self.formular_informationen:
            return self.request.principal.id
        username = self.formular_informationen.get('clearname')
        return username or self.request.principal.id
