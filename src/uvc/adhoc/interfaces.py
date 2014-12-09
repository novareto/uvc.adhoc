# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope.schema import TextLine
from uvc.tbskin.skin import ITBSkin
from zope.interface import Interface
from zope.container.interfaces import IContainer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IAdHocIdReference(Interface):
    """ Marker Interface for a kind of IntID Utility
    """


class IAdHocApplication(Interface):
    """ Marker Interface for AdHoc Applications
    """


class IAdHocLayer(IDefaultBrowserLayer):
    """ Layer which is applied to AdHoc Applications
    """


class IAdHocSkin(IAdHocLayer):
    """ Skin for IADHocApplications
    """
    grok.skin('adhoc')


class IAdHocDocumentInfo(Interface):
    """ Adapter for Extending a Principal with
        special AdHocInformation
    """

    def getAddLink():
        """Returns the AddLink for this object
        """

    def getDateFolder():
        """Returns the Folder which holds the Object
        """

    def formular_informationen():
        """Returns Information about the specific Formular
        """


class IAdHocManagement(Interface):
    """ Utility which holds the connection Stubs
        to the service backend for adhoc offers
    """


class IAdHocContent(uvcsite.IContent):
    """ Marker Interface for AdHoc Content Types
    """
    title = TextLine(
        title = u"Titel",
        description = u"Dieses Dokument erscheint dann unter dem Titel in Mein Ordner.",
        readonly = True,
        required = True)

    docid = TextLine(title=u'docid')


class IAdHocProductFolder(IContainer):
    """ Marker Interface for AdHoc Content Types
    """
