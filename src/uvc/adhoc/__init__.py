# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import logging

from uvc.adhoc.interfaces import (IAdHocContent, IAdHocIdReference,
    IAdHocApplication, IAdHocDocumentInfo, IAdHocProductFolder, IAdHocManagement)
from uvc.adhoc.components import AdHocContent, AdHocProductFolder, Formular
from uvc.adhoc.app import AdHocApp
from uvc.adhoc.adapters import getAdHocDocumentInfo, AdHocDocumentInfo, AdHocManagement
from uvc.adhoc.directive import content
from uvc.adhoc.views import BaseAddView


logger = logging.getLogger('uvcsite.adhoc')


def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s %s', summary, message)
