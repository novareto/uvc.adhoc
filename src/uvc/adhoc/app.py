# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import zope.component

#from uvcsite.browser.widgets import UvcRadioFieldWidget, UvcMultiChoiceFieldWidget
from uvc.adhoc.utils import AdHocIdReference
from zope.component.interfaces import IComponents
from uvc.adhoc.auth.handler import AdHocAuthenticator
from zope.pluggableauth import PluggableAuthentication
from grokcore.registries import create_components_registry
from uvc.adhoc.interfaces import IAdHocApplication, IAdHocIdReference
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.authentication.interfaces import IAuthentication
from zeam.form.ztk import customize
from zope.schema.interfaces import IDate
from zeam.form.ztk.widgets.choice import ChoiceField
from .interfaces import IAdHocLayer
from zope.interface import Interface


adhocRegistry = create_components_registry(
    name="adhocRegistry",
    bases=(zope.component.globalSiteManager, ),
)


grok.global_utility(
    adhocRegistry,
    name="adhocRegistry",
    provides=IComponents,
    direct=True,
)


def setup_pau(PAU):
    PAU.authenticatorPlugins = ('principals', )
    PAU.credentialsPlugins = (
        "cookies",
        "Zope Realm Basic-Auth",
        "No Challenge if Authenticated")


def intid_factory():
    return AdHocIdReference(attribute='docid')


class Dokumente(grok.Container):
    pass


class AdHocApp(grok.Application, grok.Container):
    grok.implements(IAdHocApplication)

    grok.local_utility(AdHocAuthenticator,
                       name=u"principals",
                       provides=IAuthenticatorPlugin)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       public=True,
                       setup=setup_pau)

    grok.local_utility(intid_factory,
                       IAdHocIdReference,
                       public=True)

    def __init__(self):
        super(AdHocApp, self).__init__()
        self['dokumente'] = Dokumente()

    def getSiteManager(self):
        current = super(AdHocApp, self).getSiteManager()
        #import pdb; pdb.set_trace() 
        #return adhocRegistry
        if adhocRegistry not in current.__bases__:
            adhocRegistry.__bases__ = tuple([x for x in adhocRegistry.__bases__ if x.__hash__() != zope.component.globalSiteManager.__hash__()])
            current.__bases__ = (adhocRegistry,) + current.__bases__ 
        else:
            if current.__bases__.index(adhocRegistry) == 1:
                current.__bases__ = current.__bases__[::-1]
        return current


@customize(origin=IDate)
def customize_size(field):
    field.valueLength = 'medium'


#class UvcRadioFieldWidget(UvcRadioFieldWidget):
#    grok.adapts(ChoiceField, Interface, IAdHocLayer)


#class UvcMultiChoiceFieldWidget(UvcMultiChoiceFieldWidget):
#    grok.adapts(ChoiceField, Interface, IAdHocLayer)
