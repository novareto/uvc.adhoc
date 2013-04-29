# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvc.adhoc import IAdHocContent, IAdHocProductFolder


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
