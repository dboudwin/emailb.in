from time import time, sleep
from inbox import Inbox
import re
import os
import html
from glob import glob
from bg import background


class emailDict(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        return value

    def __setitem__(self, key, value):
        if key not in dict.keys(self):
            dict.__setitem__(self, key, ["","",value])
        else:
            one, two, three = dict.__getitem__(self, key)
            dict.__setitem__(self, key, [two, three, value])

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return dictrepr

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

inbox = Inbox()
maildir = emailDict()
f = open('html/templates/index.html', 'r')
email_template = f.read()

@inbox.collate
def handle(to, sender, subject, body):
    p = re.compile(r"^.*?([a-zA-Z0-9-_]+)@emailb\.in.*")
    try:
        recip = p.search(str(to)).group(1)
        body = str((body[:100000] + '...message truncated for length') if len(body) > 100000 else body)
        maildir[recip] = body
        with open('/tmp/' + recip + ".html", 'w') as f:
            email_concat = ""
            for email in maildir[recip]:
                if len(email) > 0:
                    email_concat += "\n----------BEGIN EMAIL----------\n" + html.escape(email) +\
                                    "\n----------END EMAIL----------\n"
            emails = email_template.format(emails=email_concat)
            f.write(emails)
            f.close()
    except IOError:
        return

@background
def filewatcher():
    while True:
        for file in glob('/tmp/*.html'):
            if time() - os.path.getmtime(file) > 86400:
                os.remove(file)
                recip, ext = os.path.splitext(file)
                try:
                    maildir.pop(recip, None)
                except:
                    print('no key found')
        sleep(60)

filewatcher()

# Bind directly.
inbox.serve(address='0.0.0.0', port=25)
