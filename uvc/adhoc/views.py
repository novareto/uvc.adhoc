# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from uvcsite.content.views import Add
from uvc.layout.forms.components import Form
from uvc.adhoc import IAdHocApplication, IAdHocContent
from uvc.adhoc import getAdHocUserInfo, content
from uvc.adhoc.adapters import DateFolder
from zope.dottedname.resolve import resolve
from dolmen.content import schema


grok.templatedir('templates')


class LandingPage(uvcsite.Page):
    grok.name('index')
    grok.context(IAdHocApplication)

    title = u"Willkommen im AdHocManagement"
    description = u"Beschreibung Beschreibung"

    def namespace(self):
        ahm = getAdHocUserInfo(self.request.principal, self.request)
        return dict(ahm = ahm, ahfi = ahm.formular_informationen) 


class BaseAddView(Add):
    grok.context(DateFolder)
    grok.require('zope.View')
    grok.baseclass()

    def create(self, data):
        content_object = content.bind().get(self)
        if content:
            return resolve(content_object)()

    @property
    def fields(self):
        content_object = content.bind().get(self)
        schemas = schema.bind().get(resolve(content_object))
        return uvcsite.Fields(*schemas)

    def nextURL(self):
        self.flash(u'Added Content')
        return self.url(self.context, self.request.principal.id)
