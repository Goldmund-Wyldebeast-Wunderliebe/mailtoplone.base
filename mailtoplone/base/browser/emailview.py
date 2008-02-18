# -*- coding: utf-8 -*-
#
# File: emailview.py
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

from zope.interface import implements, Interface
from zope import component

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

from mailtoplone.base import baseMessageFactory as _
from mailtoplone.base.interfaces import IEmail
from mailtoplone.base.interfaces import IBodyFactory

class IEmailView(Interface):
    """
      EmailView interface
    """
    
    def test():
        """ test method"""
    

            
class EmailView(BrowserView):
    """
    EmailView for having a nice representation of the Email
    """
    implements(IEmailView)
        
    def __init__(self, context, request):
        # do stuff which is always needed here (convert data to email object e.g.)
        self.context = context
        self.request = request

    render = ViewPageTemplateFile('emailview.pt')

    def __call__(self):
        if self.request.get("download"):
            pass
            # do download here
        else:
            return self.render()

    @property
    def title(self):
        return self.context.title
    
    @memoize
    def headers(self):
        headerlist = ['Subject','From','To','CC']
        m = email.message_from_string(self.context.data)
        for name in headerlist:
            if m.has_key(name):
                header = ""
                for item in decode_header(m[name]):
                    try:
                        if header == "":
                            header = header + item[0].decode(item[1]).encode('utf-8')
                        else:
                            header = header + " " +item[0].decode(item[1]).encode('utf-8')
                    except (LookupError, TypeError):
                        if header == "":
                            header = header + item[0]
                        else:
                            header = header + " " +item[0]
                yield dict( name=name, content=header)


    def getAttachmentById(self, id):
        """ this results in a file-like object and mimetype """
        return file("/tmp/muha.txt"), "text/plain"


    def attachments(self):
        """return a generator which yields dicts like
            { "mimetype": "text/plain",
              "id":       "someidwhichisunique",
              "filename": "muha.txt" }
        """
        pass
        #yield dict(
        #        mimetype='text/plain',
        #        filename='filexy.txt',
        #        id='boundaryidosonstiggeid',
        #        download_url="http://www.web.de"
        #        )
        #for part in email.walk():
        #    if part.is_attachment():
        #        boundary_id = part.getid()
        #        # use urlquote here (urllib.urlquote)
        #        url="%s/view?download=%s&mimetype=%s&filename=%s" % (
        #                self.context.absolute_url(),
        #                boundary_id,
        #                mimetype,
        #                fn )

        #        yield dict(
        #                mimetype=mimetype,
        #                filename=fn,
        #                id=boundary_id,
        #                download_url=url
        #                )


    @memoize
    def body(self):
        bodyfactory = component.getUtility(IBodyFactory)
        body, content_type, charset = bodyfactory(self.context.data)
        try:
            body = body.decode(charset).encode('utf-8')
        except (LookupError, TypeError):
            pass
        return body

    
    def test(self):
        """ 
        test method 
        """
        dummy = _(u'a dummy string')
        
        return {'dummy': dummy}

# vim: set ft=python ts=4 sw=4 expandtab :
