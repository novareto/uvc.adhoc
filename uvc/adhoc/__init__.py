# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import logging

from uvc.adhoc.interfaces import (IAdHocContent, IAdHocIdReference,
    IAdHocApplication, IAdHocUserInfo, IAdHocProductFolder)
from uvc.adhoc.components import AdHocContent, AdHocProductFolder
from uvc.adhoc.app import AdHocApp
from uvc.adhoc.adapters import getAdHocUserInfo, AdHocUserInfo
from uvc.adhoc.directive import content
from uvc.adhoc.views import BaseAddView


logger = logging.getLogger('uvc.adhoc')


def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s %s', summary, message)
