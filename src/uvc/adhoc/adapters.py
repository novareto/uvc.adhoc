# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import time

from zope.component import getUtility
from zope.component import getMultiAdapter
from uvc.adhoc.interfaces import IAdHocDocumentInfo, IAdHocManagement
from zope.security.interfaces import IPrincipal
from zope.publisher.interfaces.http import IHTTPRequest
from uvc.adhoc import IAdHocIdReference
from uvc.adhoc.components import AdHocProductFolder, Formular


class AdHocManagement(grok.Adapter):
    grok.context(IPrincipal)
    grok.implements(IAdHocManagement)
    grok.baseclass()

    def getData(self):
        return {}

    def checkRule(self, login):
        return True

    def validatePassword(self, given_password, saved_password):
        if given_password == saved_password:
            return True
        return False

    def getFormulare(self, id=None, type=None):
        raise NotImplementedError

    @property
    def clearname(self):
        daten = self.getUser()
        if not daten:
            return self.context.id
        username = daten.get('clearname')
        return username


def getAdHocDocumentInfo(principal, request, name):
    return getMultiAdapter((principal, request), IAdHocDocumentInfo, name=name)


class AdHocDocumentInfo(grok.MultiAdapter):
    grok.adapts(IPrincipal, IHTTPRequest)
    grok.implements(IAdHocDocumentInfo)
    grok.baseclass()

    def __init__(self, principal, request):
        self.principal = principal
        self.request = request

    def getProductFolder(self):
        base = grok.getSite()['dokumente']
        folder_name = time.strftime('%Y_%m_%d', time.localtime())
        if not folder_name in base.keys():
            base[folder_name] = AdHocProductFolder()
        return base[folder_name]

    def getAddLink(self, id, docart):
        obj = self.getObject(id)
        if obj:
            return grok.url(self.request, obj)
        datefolder = self.getProductFolder()
        data = {'form.field.docid': id}
        addlink = "@@%s" % (
            docart.replace(' ', '_'))
        return grok.url(self.request, datefolder, addlink, data=data)

    def getObject(self, id):
        util = getUtility(IAdHocIdReference)
        return util.queryObject(id)
