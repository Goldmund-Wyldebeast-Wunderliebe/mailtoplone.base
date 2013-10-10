#!/usr/bin/python

import imaplib
import optparse
import xmlrpclib
import sys

def main():
    """  """
    # setup options
    option_parser = optparse.OptionParser(
            usage="""usage:%prog[options]"""
    )

    option_parser.add_option( "-u", "--url", dest="url",
            default=None,
            help="url of the plone instance's inbox, don't forget username and password, example: http://usr:pwd@host/plonesite/inbox" )
    option_parser.add_option( "-s", "--smtp", dest="smtp_server",
            default='imap.gmail.com',
            help="SMTP server" )
    option_parser.add_option( "-t", "--port", dest="smtp_port",
            default=993,
            help="SMTP server" )
    option_parser.add_option( "-e", "--email", dest="email",
            default=None,
            help="email address or login name for SMTP server" )

    option_parser.add_option( "-p", "--password", dest="password",
            default=None,
            help="password for SMTP server" )

    (options, args) = option_parser.parse_args()

    required = ('url', 'email', 'password')
    for req in required:
        if not hasattr(options, req):
            option_parser.print_help()
            print >>sys.stderr, '\nERROR: please specify {0}'.format(req)
            return 1

    url = options.url
    smtp_server = options.smtp_server
    smtp_port = options.smtp_port
    email = options.email
    password = options.password

    mailbox = imaplib.IMAP4_SSL(smtp_server, smtp_port)
    mailbox.login(email, password)
    mailbox.select()

    typ, data = mailbox.search(None, 'UnSeen')
    mail_nums = data[0].split()
    print 'Got {0} emails'.format(len(mail_nums))

    for idx, num in enumerate(mail_nums):
        print 'Processing mail {0}/{1}'.format(idx+1, len(mail_nums))
        typ, data = mailbox.fetch(num, '(RFC822)')  # Mail is marked as read when fetched
        mail = data[0][1]
        server = xmlrpclib.Server(url)
        server.drop(mail)


    mailbox.close()
    mailbox.logout()

if __name__ == "__main__":
    main()

