# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvc.adhoc.interfaces import IAdHocContent, IAdHocProductFolder


class Formular(object):
    defaults = {}

    def __init__(self, id, type, **kwargs):
        self.id = id
        self.type = type
        self.datum = ""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def info(self):
        from uvc.adhoc.adapters import getAdHocDocumentInfo
        request = uvcsite.getRequest()
        return getAdHocDocumentInfo(request.principal, request, self.type)

    @property
    def addlink(self):
        return self.info.getAddLink(self.id, self.type)

    @property
    def productfolder(self):
        return self.info.getProductFolder()

    @property
    def getObject(self):
        return self.info.getObject(self.id)

    @property
    def title(self):
        return self.info.title

    @property
    def description(self):
        return self.info.description

    def __repr__(self):
        return "<Formular id=%s type=%s>" % (self.id, self.type)


class AdHocContent(uvcsite.Content):
    grok.implements(IAdHocContent)

    @property
    def container_id(self):
        return "%s%s" % (self.principal.id, self.docid)


class AdHocProductFolder(grok.Container):
    grok.implements(IAdHocProductFolder)

    def getContentType(self):
        return

    def getContentName(self):
        return ""

    def add(self, content):
        self[content.container_id] = content
