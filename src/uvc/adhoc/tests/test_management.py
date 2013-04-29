# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import unittest
import doctest
from zope.testing import doctest


def test_suite():
    suite = unittest.TestSuite()
    management = doctest.DocTestSuite(
        'uvc.adhoc.tests.components.management',
        optionflags=doctest.ELLIPSIS+
        doctest.NORMALIZE_WHITESPACE)
    suite.addTest(management)
    return suite
