"""Definition of the Email content type
"""
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from zope.component import getUtility, getAdapter, getMultiAdapter
from zope.interface import implements, directlyProvides
from zope.globalrequest import getRequest

from Products.Archetypes import atapi
from Products.ATContentTypes.content import file

from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from mailtoplone.base import baseMessageFactory as _
from mailtoplone.base.interfaces import IEmail
from mailtoplone.base.config import PROJECTNAME




EmailSchema = file.ATFileSchema.copy() + atapi.Schema((

# Your Archetypes field definitions here ...

))

# Set storage on fields copied from ATContentTypeSchemata, making sure 
# they work well with the python bridge properties.

EmailSchema['title'].storage = atapi.AnnotationStorage()
EmailSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(EmailSchema, moveDiscussion=False)

class Email(file.ATFile):
    """A file like content containing an email"""
    implements(IEmail)

    portal_type = "Email"
    _at_rename_after_creation = True
    schema = EmailSchema
    schema['file'].index_method = 'mail_indexer'

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def mail_indexer(self):
        request = getRequest()

        view = getMultiAdapter((self, request,), name=u"view")

        headers =  view.headers()
        indexed = [x.get('contents', '')[0] for x in headers]

        mail_body = view.body()
        mail_text = mail_body.get('text', '')

        if mail_body.get('content_type') == 'text/html':
            portal_transforms = getToolByName(self, 'portal_transforms')
            data = portal_transforms.convertTo('text/plain', mail_text, mimetype='text/html')
            mail_text = safe_unicode(data.getData())

        indexed.append(mail_text)

        searchable_text = ' '.join(indexed)

        return searchable_text

atapi.registerType(Email, PROJECTNAME)
