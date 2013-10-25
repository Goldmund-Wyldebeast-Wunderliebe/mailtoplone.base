# -*- coding: utf-8 -*-
#
# File: test_emailview.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import unittest
from zope.globalrequest import setRequest
from zope.interface.interface import InterfaceClass
from zope.publisher.browser import TestRequest
from mailtoplone.base.adapter import MailIndexer
from mailtoplone.base.content.email import EmailSchema
from mailtoplone.base.interfaces import IMailIndexer

from mailtoplone.base.tests.base import MailToPloneBaseTestCase


class TestMailIndexer(MailToPloneBaseTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))
        self.portal.invokeFactory('Email', 'm1')

    def test_file_schema(self):
        """ The mail_indexer function is set in AT schema as
            index_method on file field
        """
        schema = EmailSchema
        self.assertEqual(schema['file'].index_method, 'mail_indexer')

    def test_mail_indexer(self):
        """ Check if the mail_indexer function is present on
        an Email content type
        """
        text = self.portal['m1'].mail_indexer()
        self.assertEqual(text, '')  # No email is stored, so output is empty

    def test_adapter(self):
        """ Basic tests on the indexer adapter """
        adapter = IMailIndexer(self.portal['m1'])

        self.assertEqual(type(IMailIndexer), InterfaceClass)
        self.assertEqual(type(adapter), MailIndexer)
        self.assertTrue(hasattr(adapter, 'indexer'))  # Adapter has indexer function

        text = IMailIndexer(self.portal['m1']).index()
        self.assertEqual(text, '')  # No email is stored, so output is empty


def test_suite():
    setRequest(TestRequest())  # Set fake request on zope global request

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMailIndexer))
    return suite

# vim: set ft=python ts=4 sw=4 expandtab :

