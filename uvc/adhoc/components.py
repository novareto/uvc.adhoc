# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvc.adhoc import IAdHocContent, IAdHocProductFolder


class AdHocContent(uvcsite.Content):
    grok.implements(IAdHocContent)

    def get_uid(self):
        return int(self._uid)

    def set_uid(self, uid):
        self._uid = int(uid)
        return self._uid

    uid = property(get_uid, set_uid)

    @property
    def container_id(self):
        return "%s%s" % (self.principal.id, self.uid)


class AdHocProductFolder(grok.Container):
    grok.implements(IAdHocProductFolder)

    def getContentType(self):
        return

    def getContentName(self):
        return "RUMS"

    def add(self, content):
        self[content.container_id] = content
