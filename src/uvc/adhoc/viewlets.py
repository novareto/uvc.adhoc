# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import grok


from uvc.adhoc.interfaces import IAdHocLayer, IAdHocManagement
from uvc.layout.slots.menuviewlets import PersonalPreferencesViewlet
from grokcore.chameleon.components import ChameleonPageTemplateFile


class PersonalPreferences(PersonalPreferencesViewlet):
    grok.order(1)
    grok.name('personalpreferencesviewlet')
    grok.layer(IAdHocLayer)
    grok.require('zope.View')
    base_template = ChameleonPageTemplateFile('templates/personalpreferences.cpt')

    def render(self):
        return self.base_template.render(self)
