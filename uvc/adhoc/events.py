# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvc.adhoc import IAdHocContent
from zope.component import getUtility
from uvc.adhoc.interfaces import IAdHocIdReference
from uvcsite.workflow.basic_workflow import PUBLISHED
from hurry.workflow.interfaces import IWorkflowTransitionEvent
from zope.securitypolicy.interfaces import IPrincipalPermissionManager


@grok.subscribe(IAdHocContent, grok.IObjectAddedEvent)
def handle_add(obj, event):
    refs = getUtility(IAdHocIdReference)
    refs.register(obj)


@grok.subscribe(IWorkflowTransitionEvent)
def add_view_permission(event):
    obj = event.object
    if not IAdHocContent.providedBy(obj):
        return
    if event.destination == PUBLISHED:
        ppm = IPrincipalPermissionManager(obj)
        ppm.grantPermissionToPrincipal('uvc.ViewContent', obj.principal.id)
