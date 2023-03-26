import imaplib
import email
import logging
from time import sleep

from settings import config

client = None

def login(username, password):
    imap_config = config['imap']
    try:
        global client
        logging.info('Connect to imap server with account=%s and password=%s' % 
                    (username, password))
        client = imaplib.IMAP4_SSL(imap_config['host'], int(imap_config['port']))
        client.login(username, password)
        return client
    except Exception as ex:
        logging.exception('An exception happens while connecting to imap server.')
        raise ex

def logout():
    global client
    if(client is not None):
        logging.info('Disconnect to imap server.')
        client.close()
        client.logout()

# Delete all mails from the mail inbox
def clear_inbox():
    if client is None:
        raise Exception('Pls invoke login first to set up connection to imap server.')
    try:
        # Remove all emails
        client.select('Inbox')
        logging.info('Clear all e-mails in the inbox')
        result, data = client.uid('search', None, 'All')
        uids = data[0].split()
        if result!='OK':
            raise Exception('Failed to search all e-mails.')
        for uid in uids:
            client.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
    except Exception as e:
        raise e

# Search email from the inbox, return the mail content
def search_email(subject, sender, timeout=60):
    # Get the content from the email message
    def get_email_content(email_messsage):
        maintype = email_message.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message.get_payload()

    if client is None:
        raise Exception('Pls call login first to set up connection to your mailbox')
    
    client.select('Inbox')

    search_condition = '(HEADER Subject "%s" FROM "%s")' % (subject, sender)

    try:
        logging.info('Search e-mails with the condition:%s' % search_condition)
        i = 0
        while(i<timeout):
            sleep(2)
            _, data = client.uid('search', None, search_condition)
            results_length = len(data[0].split())
            if results_length == 1:  # Found the e-mail that matches the search condition
                email_uid = data[0].split()[-1]
                _, data = client.uid('fetch', email_uid, '(RFC822)')
                # Convert raw bytes message to readable e-mail message
                email_message= email.message_from_bytes(data[0][1])
                content = get_email_content(email_message)
                return (True, content)
            elif results_length>1:
                logging.error('Multiple e-mails returned with the condition, pls manually check the inbox.')
                raise Exception('More than one e-mail are retrived with the search condition,'  
                                'pls check the Inbox manually')
            else:
                i = i + 2
        logging.error("Cannot find the matched e-mail, pls manually check the inbox.")
        return (False, 'Time out, the e-mail can still not be retrived with the search condition: %s' % search_condition)
    except Exception as ex:
        logging.exception('An exception happens while searching e-mails.')
        raise ex