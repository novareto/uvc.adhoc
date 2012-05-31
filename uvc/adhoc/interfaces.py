# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import uvcsite

from zope.interface import Interface
from zope.container.interfaces import IContainer


class IAdHocIdReference(Interface):
    """ Marker Interface for a kind of IntID Utility
    """


class IAdHocApplication(Interface):
    """ Marker Interface for AdHoc Applications
    """


class IAdHocUserInfo(Interface):
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


class IAdHocProductFolder(IContainer):
    """ Marker Interface for AdHoc Content Types
    """
