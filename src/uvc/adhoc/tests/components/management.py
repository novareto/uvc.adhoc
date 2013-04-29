"""
  >>> from grokcore.json import testing
  >>> testing.grok(__name__)

  >>> AZ = "100000"
  >>> principal = Principal(AZ, AZ)

  >>> ahm = uvc.adhoc.IAdHocManagement(principal)
  >>> ahm
  <uvc.adhoc.tests.components.management.MyAdHocManagement object at ...>

"""

import uvc.adhoc
from zope.pluggableauth.factories import Principal


class MyAdHocManagement(uvc.adhoc.AdHocManagement):

    def getUser(self):
        return {}
