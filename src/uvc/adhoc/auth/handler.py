# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import zope.security

from uvc.adhoc.interfaces import IAdHocManagement
from zope.session.interfaces import ISession
from zope.pluggableauth.factories import PrincipalInfo
from zope.pluggableauth.interfaces import IAuthenticatorPlugin


USER_SESSION_KEY = "adhoc.authentication"


class AdHocAuthenticator(grok.Model):
    """ Custom Authenticator for UVC-Site"""
    grok.implements(IAuthenticatorPlugin)
    prefix = 'adhoc.principals.'

    def authenticateCredentials(self, credentials):
        """
        Check if username and password match
        get the credentials from the IUserManagement Utility
        """
        request = zope.security.management.getInteraction().participations[0]
        session = ISession(request)['adhoc.authentication']
        authenticated = session.get(USER_SESSION_KEY)
        if authenticated is None:
            if not (credentials and 'login' in credentials
                    and 'password' in credentials):
                return
            login, password = credentials['login'], credentials['password']

            utility = IAdHocManagement(request.principal)

            if not utility.checkRule(login):
                return

            user = utility.getData(login)
            print user
            if not user:
                return

            if not utility.validatePassword(password, user.get('password')):
                return
            user_id = login
            authenticated = session[USER_SESSION_KEY] = dict(
                id=user_id,
                title=login,
                description=login,
                login=login)
        return PrincipalInfo(**authenticated)

    def principalInfo(self, id):
        """we don´t need this method"""
        if id.startswith('uvc.'):
            return PrincipalInfo(id, id, id, id)
