# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import time
import uvcsite

from zope.component import getUtility
from zope.component import getMultiAdapter
from uvc.adhoc.interfaces import IAdHocDocumentInfo, IAdHocManagement
from zope.security.interfaces import IPrincipal
from zope.publisher.interfaces.http import IHTTPRequest
from uvc.adhoc import AdHocProductFolder, IAdHocIdReference


class Formular(object):

    def __init__(self, id, type, **kwargs):
        self.id = id
        self.type = type
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def info(self):
        request = uvcsite.getRequest()
        return getAdHocDocumentInfo(request.principal, request, self.type)

    @property
    def addlink(self):
        return self.info.getAddLink(self.id, self.type)

    @property
    def productfolder(self):
        return self.info.getProductFolder()

    def __repr__(self):
        return "<Formular id=%s type=%s>" % (self.id, self.type)


class AdHocManagement(grok.Adapter):
    grok.context(IPrincipal)
    grok.implements(IAdHocManagement)
    grok.baseclass()

    def getData(self):
        return {}

    def validatePassword(self, given_password, saved_password):
        if given_password == saved_password:
            return True
        return False

    def getFormulare(self, id=None, type=None):
        rc = []
        formulare = self.getData().get('formulare', [])
        for formular in formulare:
            fc = Formular(
                id=formular.get('id'),
                type=formular.get('type'),
                defaults=formular.get('defaults'),
            )
            if id:
                if formular.get('id') == id:
                    rc.append(fc)
            elif type:
                if formular.get('type') == type:
                    rc.append(fc)
            else:
                rc.append(fc)
        return rc

    @property
    def clearname(self):
        daten = self.getUser()
        if not daten:
            return self.context.id
        username = daten.get('clearname')
        return username or self.request.principal.id


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
        if not isinstance(id, int):
            if not id.isdigit():
                return
        return util.queryObject(int(id))
