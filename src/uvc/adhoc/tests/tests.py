# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import unittest
import doctest
import StringIO

from uvcsite.tests import product_config
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer

import uvc.adhoc.tests
import zope.app.appsetup


class AdHocLayer(ZopeFanstaticBrowserLayer):

    def __init__(self, *args, **kw):
        self.conf = zope.app.appsetup.product.loadConfiguration(
            StringIO.StringIO(kw.pop('product_config', '')))
        self.conf = [
            zope.app.appsetup.product.FauxConfiguration(name, values)
            for name, values in self.conf.items()]
        super(AdHocLayer, self).__init__(*args, **kw)

    def setUp(self):
        zope.app.appsetup.product.setProductConfigurations(self.conf)
        zope.app.wsgi.testlayer.BrowserLayer.setUp(self)


browser_layer = AdHocLayer(uvc.adhoc.tests, product_config=product_config)


def test_suite():
    suite = unittest.TestSuite()

    app_test = doctest.DocFileSuite(
        'README.txt', 'UTILITY.txt',
        optionflags=(
            doctest.ELLIPSIS +
            doctest.NORMALIZE_WHITESPACE +
            doctest.REPORT_NDIFF),
        globs={'getRootFolder': browser_layer.getRootFolder})
    app_test.layer = browser_layer

    suite.addTest(app_test)
    return suite
