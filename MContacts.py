#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import getopt
import getpass
import atom
import gdata.data
import gdata.contacts.data
import gdata.contacts.client
import json
import os
import Log


class MContacts:
  def __init__(self, email, password):
    self.gd_client = gdata.contacts.client.ContactsClient(source='GoogleInc-ContactsPythonSample-1')
    self.gd_client.ClientLogin(email, password, self.gd_client.source)
    self.Contacts = []
    self.Log = Logs()
    

  def PrintPaginatedFeed(self, feed, print_method):
    ctr = 0
    while feed:
      # Print contents of current feed
      ctr = print_method(feed=feed, ctr=ctr)
      # Prepare for next feed iteration
      next = feed.GetNextLink()
      feed = None
      if next:
         feed = self.gd_client.GetContacts(uri=next.href)
        

  def SaveContacts(self):
    try:
        feed = self.gd_client.GetContacts()
        
        self.PrintPaginatedFeed(feed, self.PrintContactsFeed)
        simplejson = json
        f = open("Contacts.txt", "w")
        simplejson.dump(self.Contacts, f)
        f.close()
    except Exception as ex:
        self.Log.writelog("SaveContacts %s" % str(ex))
        return -1
    return 1

  def PrintContactsFeed(self, feed, ctr):
    if not feed.entry:
      self.Log.writelog('\nNo contacts in feed.\n')
      return 0
    for i, entry in enumerate(feed.entry):
      Contact = []
      if not entry.name is None:
        family_name = entry.name.family_name is None and " " or entry.name.family_name.text.encode('utf8')
        full_name = entry.name.full_name is None and " " or entry.name.full_name.text.encode('utf8')
        given_name = entry.name.given_name is None and " " or entry.name.given_name.text.encode('utf8')
        try:
            Contact.append(full_name)
            for x, e in enumerate(entry.phone_number):
                try:
                    tel = e is None and " " or e.text
                    Contact.append(tel)
                except Exception as ex:
                    self.Log.writelog("Error2: %s" % str(ex))
            self.Contacts.append(Contact)
           # print Contact[0] + " " + str(len(self.Contacts))
        except Exception as ex:
            self.Log.writelog("Error3: %s" % str(ex))
        
      else:
        self.Log.writelog('\n%s %s (title)' % (ctr + i + 1, entry.title.text))
    return len(feed.entry) + ctr
