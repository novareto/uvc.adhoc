# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from dolmen.content import schema
from zeam.form.base import DictDataManager
from zope.dottedname.resolve import resolve
from dolmen.forms.base import set_fields_data
from uvcsite.content.views import Add, Display
from zope.traversing.browser import absoluteURL
from uvc.adhoc import getAdHocUserInfo, content
from hurry.workflow.interfaces import IWorkflowState
from uvcsite.workflow.basic_workflow import titleForState
from megrok.z3ctable import TablePage, Column, GetAttrColumn, LinkColumn
from uvc.adhoc import IAdHocProductFolder, IAdHocApplication, IAdHocContent


grok.templatedir('templates')


class LandingPage(uvcsite.Page):
    grok.name('index')
    grok.context(IAdHocApplication)

    title = u"Willkommen im AdHocManagement"
    description = u"Beschreibung Beschreibung"

    def namespace(self):
        ahm = getAdHocUserInfo(self.request.principal, self.request)
        return dict(
            ahm=ahm,
            obj=ahm.getObject(),
            ahfi=ahm.formular_informationen,
            )


class BaseAddView(Add):
    grok.context(IAdHocProductFolder)
    grok.require('zope.View')
    grok.baseclass()

    ignoreContent = False

    @property
    def defaults(self):
        ahui = getAdHocUserInfo(
            self.request.principal, self.request)
        return ahui.formular_informationen.get('defaults', {})

    @property
    def fields(self):
        content_object = content.bind().get(self)
        schemas = schema.bind().get(resolve(content_object))
        return uvcsite.Fields(*schemas)

    def update(self):
        self.setContentData(
            DictDataManager(self.defaults))

    def create(self, data):
        content_object = content.bind().get(self)
        if content_object:
            obj = resolve(content_object)()
            set_fields_data(self.fields, obj, data)
            return obj

    def nextURL(self):
        self.flash(u'Added Content')
        return self.url(self.context, self.request.principal.id)


class BaseView(Display):
    grok.name('index')
    grok.context(IAdHocContent)

    ignoreContent = False

    @property
    def fields(self):
        return uvcsite.Fields(*self.context.schema)


class DisplayProductFolderListing(TablePage):
    grok.title(u'AdHoc Objekte')
    grok.name('index')
    grok.context(IAdHocProductFolder)

    cssClasses = {'table':
        'tablesorter table table-striped table-bordered table-condensed'}


class Link(LinkColumn):
    grok.name('link')
    grok.context(IAdHocProductFolder)
    weight = 1
    header = u"Titel"
    linkName = u"edit"

    def getLinkURL(self, item):
        """Setup link url."""
        state = IWorkflowState(item).getState()
        if state != None:
            state = titleForState(state)
        if self.linkName is not None and state == "Entwurf":
            return '%s/%s' % (absoluteURL(item, self.request), self.linkName)
        return absoluteURL(item, self.request)

    def getLinkContent(self, item):
        return item.title


class MetaTypeColumn(GetAttrColumn):
    header = u'Objekt'
    grok.name('meta_type')
    grok.context(IAdHocProductFolder)
    attrName = 'meta_type'
    weight = 2


class CreatorColumn(Column):
    grok.context(IAdHocProductFolder)
    grok.name('creator')
    header = u"Autor"
    weight = 99

    def renderCell(self, item):
        return item.principal.id


class ModifiedColumn(Column):
    grok.context(IAdHocProductFolder)
    grok.name('modified')
    header = u"Datum"
    weight = 100

    def renderCell(self, item):
        return uvcsite.fmtDateTime(item.modtime)


class StateColumn(GetAttrColumn):
    grok.context(IAdHocProductFolder)
    grok.name('state')
    header = u'Status'
    attrName = 'status'
    weight = 3

    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state != None:
            return titleForState(state)
        return self.defaultValue
