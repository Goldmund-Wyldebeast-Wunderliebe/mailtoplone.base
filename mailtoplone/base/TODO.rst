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
  BodyFactory returns charset ( None if it isn't specified)
  use return charset to decode(charset) and encode as utf-8
  returned charset might be not an available charset for decoding, 
  in this case don't decode / encode

- create download for attachments

 vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
