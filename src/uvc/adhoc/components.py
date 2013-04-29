# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvc.adhoc import IAdHocContent, IAdHocProductFolder


class Formular(object):

    def __init__(self, id, docart, titel, beschreibung=u"", defaults={}):
        self.id = id
        self.docart = docart
        self.titel = titel
        self.beschreibung = beschreibung
        self.defaults = defaults


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
