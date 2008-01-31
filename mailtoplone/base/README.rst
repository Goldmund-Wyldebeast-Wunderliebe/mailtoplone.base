mailtoplone.base
================

Setup TestEnvironment
---------------------

Setting up a inbox containing email1, email2::

    >>> self.setRoles(('Manager',))
    >>> self.portal.invokeFactory('InBox', 'inbox')
    'inbox'
    >>> self.portal.inbox.invokeFactory('Email', 'email1')
    'email1'
    >>> self.portal.inbox.invokeFactory('Email', 'email3')
    'email3'

Adapter
-------

Let's test the drop function useable with the MailDropBox Adapter,
The dropped mails should fill the gaps in the id naming convention::

    >>> from mailtoplone.base.interfaces import IMailDropBox
    >>> IMailDropBox(self.portal.inbox).drop("some data")
    >>> IMailDropBox(self.portal.inbox).drop("some data")
    >>> IMailDropBox(self.portal.inbox).drop("some data")
    >>> self.portal.inbox.objectIds()
    ['email1', 'email3', 'email', 'email0', 'email2']

Let's test some values of a created email::

    >>> self.portal.inbox.email0.title
    'email0'
    >>> self.portal.inbox.email0.data
    'some data'
    >>> self.portal.inbox.email0.meta_type
    'Email'


Browserview xmlrpcview
----------------------

Let's test if the xmlrpcview has a drop method which creates an Email in
the inbox::

    >>> theview = self.portal.inbox.restrictedTraverse('xmlrpcview')
    >>> theview.drop("dropped via view")
    >>> self.portal.inbox.objectIds()
    ['email1', 'email3', 'email', 'email0', 'email2', 'email4']
    >>> self.portal.inbox.email4.data
    'dropped via view'





::

    vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:

