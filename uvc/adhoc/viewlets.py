# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok


from uvc.adhoc.interfaces import IAdHocLayer
from uvc.adhoc.adapters import getAdHocUserInfo
from uvc.layout.slots.menuviewlets import PersonalPreferencesViewlet


class PersonalPreferences(PersonalPreferencesViewlet):
    grok.order(1)
    grok.name('personalpreferencesviewlet')
    grok.layer(IAdHocLayer)

    @property
    def username(self):
        return getAdHocUserInfo(self.request.principal, self.request).clearname
