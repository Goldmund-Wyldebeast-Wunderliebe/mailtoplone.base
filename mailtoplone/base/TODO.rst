mailtoplone base TODO
=====================

:Author:    $Author$
:Date:      $Date$
:Revision:  $Revision$

emailview
---------

- decode headers::

  from email.Header import decode_header
  yield dict( name=name, content=[header for header in decode_header(m[name])])

- body needs to be decoded also,
  therefore need to determine encoding of body
  change BodyFactory utility to extract the charset for the
  returned body and return, body, content_type, charset

- create download for attachments

 vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
