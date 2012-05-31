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

  >>> from uvc.adhoc import IAdHocProductFolder
  >>> adhocuserinfo = getAdHocUserInfo(christian, request)
  >>> adhocuserinfo
  <MyAdHocUserInfo object at ...>

  >>> p_folder = adhocuserinfo.getProductFolder()
  >>> p_folder
  <uvc.adhoc.components.AdHocProductFolder object at 0...>

  >>> IAdHocProductFolder.providedBy(p_folder)
  True

  >>> len(dokumente)
  1

  >>> len(p_folder)
  0

  >>> adhocuserinfo.getAddLink()
  'http://127.0.0.1/app/dokumente/.../@@wiederaufnahme_der_arbeit'


Content
-------

  >>> from uvc.adhoc import AdHocContent, IAdHocContent
  >>> waa = AdHocContent()
  >>> waa
  <uvc.adhoc.components.AdHocContent object at ...>

  >>> IAdHocContent.providedBy(waa)
  True

  >>> p_folder.add(waa)

  >>> len(p_folder)
  1

  >>> p_folder.get(request.principal.id)
  <uvc.adhoc.components.AdHocContent object at ...>


Workflow
--------

  >>> from hurry.workflow.interfaces import IWorkflowState
  >>> IWorkflowState(waa).getState()
  0

Security
--------

  >>> from zope.securitypolicy.interfaces import IPrincipalPermissionManager
  >>> ppm = IPrincipalPermissionManager(waa)
  >>> ppm.getPermissionsForPrincipal(waa.principal.id)
  []

  >>> from hurry.workflow.interfaces import IWorkflowInfo
  >>> IWorkflowInfo(waa).fireTransition('publish')
  >>> ppm = IPrincipalPermissionManager(waa)
  >>> ppm.getPermissionsForPrincipal(waa.principal.id)
  [('uvc.ViewContent', PermissionSetting: Allow)]


IntIds
------

  >>> from zope.component import getUtility
  >>> from uvc.adhoc.interfaces import IAdHocIdReference 
  >>> refs = getUtility(IAdHocIdReference)
  >>> ref_obj = refs.queryObject(int(request.principal.id))
  >>> ref_obj
  <uvc.adhoc.components.AdHocContent object at 0...>

  >>> ref_obj is waa
  True

  >>> ref_obj.__parent__ is p_folder
  True

  >>> endInteraction()
