=======
Doctest
=======

uvc.adhoc

:Test-Layer: functional

Setup
-----

  >>> from uvc.adhoc import AdHocApp, IAdHocUserInfo
  >>> from zope.component.hooks import setSite
  >>> from zope.pluggableauth.factories import Principal
  >>> from zope.publisher.browser import TestRequest
  >>> root = getRootFolder()
  >>> root['app'] = app = AdHocApp() 

  >>> setSite(app)

  >>> app
  <uvc.adhoc.app.AdHocApp object at 0...>

  >>> dokumente = app['dokumente']
  >>> dokumente
  <uvc.adhoc.app.Dokumente object at 0...>

  >>> len(dokumente)
  0

  >>> christian = Principal('christian', 'christian')
  >>> christian
  Principal('christian')

  >>> from uvcsite.tests import startInteraction, endInteraction
  >>> request = startInteraction('12345678') 
  >>> from uvc.adhoc import getAdHocUserInfo, AdHocUserInfo

  >>> class MyAdHocUserInfo(AdHocUserInfo):
  ...     @property
  ...     def formular_informationen(self):
  ...         return dict(
  ...            titel = u"Wiederaufnahme der Arbeit",
  ...            beschreibung = u"Wann haben Sie nach Ihrem Unfall die Arbeit wieder aufgenommen",
  ...            defaults = {},
  ...            icon = "fanstatic/uvc.ahex/unfallanzeige.png",
  ...            )

  >>> from grokcore.component.testing import grok_component
  >>> grok_component('MyAdHocUserInfo', MyAdHocUserInfo)
  True



  >>> adhocuserinfo = getAdHocUserInfo(christian, request)
  >>> adhocuserinfo
  <MyAdHocUserInfo object at ...>

  >>> date_folder = adhocuserinfo.getDateFolder()
  >>> date_folder
  <uvc.adhoc.adapters.DateFolder object at 0...>

  >>> len(dokumente)
  1

  >>> len(date_folder)
  0

  >>> adhocuserinfo.getAddLink()
  'http://127.0.0.1/app/dokumente/.../@@wiederaufnahme_der_arbeit'


Content
-------

  >>> from uvc.adhoc import AdHocContent
  >>> waa = AdHocContent()
  >>> from zope.component import getUtility
  >>> from zc.intid import IIntIds
  >>> iiutil = getUtility(IIntIds)
  >>> iiutil.register(waa)
  >>> iiutil.register(waa)
  >>> import pdb; pdb.set_trace() 
  


IntIds
------


  >>> endInteraction()
