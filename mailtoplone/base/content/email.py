"""Definition of the Email content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import file

from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from mailtoplone.base.interfaces import IEmail, IMailIndexer
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
        """ Use the MailIndexer adapter for indexing emails, returned text is
         stored as SearchableText in the portal catalog.
        """
        return IMailIndexer(self).index()

atapi.registerType(Email, PROJECTNAME)
