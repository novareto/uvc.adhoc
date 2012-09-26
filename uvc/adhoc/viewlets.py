# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok


from uvc.adhoc.interfaces import IAdHocLayer, IAdHocManagement 
from uvc.layout.slots.menuviewlets import PersonalPreferencesViewlet


class PersonalPreferences(PersonalPreferencesViewlet):
    grok.order(1)
    grok.name('personalpreferencesviewlet')
    grok.layer(IAdHocLayer)

    @property
    def username(self):
        return IAdHocManagement(self.request.principal).clearname
