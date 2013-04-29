# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import BTrees
import persistent
import zope.security.proxy

from uvc.adhoc.interfaces import IAdHocIdReference


unwrap = zope.security.proxy.removeSecurityProxy


class AdHocIdReference(persistent.Persistent):
    """This utility provides a two way mapping between objects and
    integer ids.

    The objects are stored directly in the internal structures.

    """

    grok.implements(IAdHocIdReference)
    family = BTrees.family32

    def __init__(self, attribute, family=None):
        if family is not None:
            self.family = family
        self.attribute = attribute
        self.refs = self.family.IO.BTree()

    def __len__(self):
        return len(self.refs)

    def items(self):
        return list(self.refs.items())

    def __iter__(self):
        return self.refs.iterkeys()

    def getObject(self, id):
        return self.refs[id]

    def queryObject(self, id, default=None):
        if id in self.refs:
            return self.refs[id]
        return default

    def getId(self, ob):
        unwrapped = unwrap(ob)
        uid = getattr(unwrapped, self.attribute, None)
        if uid is None:
            raise KeyError(ob)
        return int(uid)

    def register(self, ob):
        ob = unwrap(ob)
        uid = self.getId(ob)
        if uid is None:
            print "THIS UID IS ALREADY THERE"
        self.refs[uid] = ob
        return uid

    def unregister(self, ob):
        ob = unwrap(ob)
        uid = self.getId(ob)
        if uid is None:
            return
        del self.refs[uid]
