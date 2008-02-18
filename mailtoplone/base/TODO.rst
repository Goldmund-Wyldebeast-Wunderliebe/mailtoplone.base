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

- create download for attachments

 vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
