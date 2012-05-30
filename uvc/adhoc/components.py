# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from uvc.adhoc import IAdHocContent

class AdHocContent(uvcsite.Content):
    grok.implements(IAdHocContent)

    def get_principal_id(self):
        return int(self.principal.id)

    def set_principal_id(self, full_name):
        return int(self.principal.id)

    principal_id = property(get_principal_id, set_principal_id)
