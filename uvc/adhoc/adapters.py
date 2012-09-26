# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import time
import uvcsite

from zope.interface import Interface
from zope.component import getUtility
from zope.component import getMultiAdapter
from uvc.adhoc.interfaces import IAdHocDocumentInfo, IAdHocManagement
from zope.security.interfaces import IPrincipal
from zope.publisher.interfaces.http import IHTTPRequest
from uvc.adhoc import AdHocProductFolder, IAdHocIdReference


class AdHocManagement(grok.Adapter):
    grok.context(IPrincipal)
    grok.implements(IAdHocManagement)
    grok.baseclass()

    def getUser(self):
        return {}

    def getFormulare(self):
        ahms = self.getUser().get('documents', [])
        request = uvcsite.utils.shorties.getRequest()
        for ahm in ahms:
            ahfm = getAdHocDocumentInfo(self.context, request, ahm, name=ahm.get('docart'))
            yield ahfm

    def getFormularById(self, id):
        for ahm in self.getFormulare():
            if grok.name.bind().get(ahm) == id:
                return ahm
        return 

    @property
    def clearname(self):
        daten = self.getUser()
        if not daten:
            return self.context.id
        username = daten.get('clearname')
        return username or self.request.principal.id



def getAdHocDocumentInfo(principal, request, ahm, name):
    return getMultiAdapter((principal, request, ahm), IAdHocDocumentInfo, name=name)


class AdHocDocumentInfo(grok.MultiAdapter):
    grok.adapts(IPrincipal, IHTTPRequest, Interface)
    grok.implements(IAdHocDocumentInfo)
    grok.baseclass()

    icon = u""
    title = u""
    description = u""

    def __init__(self, principal, request, ahm):
        self.principal = principal
        self.request = request
        self.ahm = ahm

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
            self.ahm.get('docart').replace(' ', '_').lower())
        return grok.url(self.request, datefolder, addlink)

    def getObject(self):
        util = getUtility(IAdHocIdReference)
        if not self.principal.id.isdigit():
            return
        return util.queryObject(int(self.principal.id))
