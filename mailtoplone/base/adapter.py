# -*- coding: utf-8 -*-
#
# File: adapter.py
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

__author__    = """Hans-Peter Locher<hans-peter.locher@inquant.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: 36831 $"
__version__   = '$Revision: 1.7 $'[11:-2]

import email
from email.Header import decode_header

from zope import interface, component
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.event import notify
try:
    from zope.container.interfaces import INameChooser
except ImportError:
    # Plone 4.2 (and older) compatibility
    from zope.app.container.interfaces import INameChooser
from plone.i18n.normalizer.interfaces import IIDNormalizer

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from mailtoplone.base.interfaces import IMailDropBox, IMailIndexer
from mailtoplone.base.events import MailDroppedEvent

DEFAULT_ID = 'email'

class MailDropBox(object):
    """ adapts a IMailDropBoxMarker to a IMailDropBox """

    interface.implements(IMailDropBox)

    def __init__(self, context):
        self.context = context

    def drop(self, mail):
        """ drop a mail into this mail box. The mail is
        a string with the complete email content """
        
        # code unicode to utf-8
        if isinstance(mail,unicode):
            mail = mail.encode( 'utf-8' )
        type = 'Email'
        format = 'text/plain'
        content_type='text/plain'

        #generate title
        mailobj = email.message_from_string(mail)
        # Subject
        for key in "Subject subject Betreff betreff".split():
            subject = mailobj.get(key)
            if subject:
                subject = self.decodeheader(subject)
                break

        id = subject or DEFAULT_ID
        title = id

        # generate id
        normalizer = component.getUtility(IIDNormalizer)
        chooser = INameChooser(self.context)
        id = chooser.chooseName(normalizer.normalize(id), aq_base(self.context))

        self.context.invokeFactory(type ,id=id , title=title, format=format, \
                                   content_type=content_type, file=mail)
        getattr(self.context, id, None).setContentType(content_type)
        getattr(self.context, id, None).processForm()
        notify(MailDroppedEvent(getattr(self.context, id, None), self.context))

    def decodeheader(self, header_text, default="ascii"):
        """Decode the specified header"""
        headers = decode_header(header_text)
        header_sections = [unicode(text, charset or default)
                       for text, charset in headers]
        return u"".join(header_sections)


class MailIndexer(object):
    """ This adapter extracts searchable text from an email. The email body
     and email headers (from, to, subject etc.) are indexed.
    """

    interface.implements(IMailIndexer)

    def __init__(self, context):
        self.context = context

    def index(self):

        request = getRequest()

        view = getMultiAdapter((self.context, request,), name=u"view")

        headers =  view.headers()
        indexed = [x.get('contents', '')[0] for x in headers]

        mail_body = view.body()
        mail_text = mail_body.get('text', '')

        if mail_body.get('content_type') == 'text/html':
            portal_transforms = getToolByName(self.context, 'portal_transforms')
            data = portal_transforms.convertTo('text/plain', mail_text, mimetype='text/html')
            mail_text = safe_unicode(data.getData())

        indexed.append(mail_text)

        searchable_text = ' '.join(indexed)

        return searchable_text


# vim: set ft=python ts=4 sw=4 expandtab :
