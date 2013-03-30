#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os

class Logs():
    def __init__(self, filename= "logfile", printtooutput=True,curdir=os.getcwd()):
        self.name = filename
        self.printtooutput = printtooutput
        self.curdir =curdir
    def writelog(self, s):
        
        flag = 0
        f = ''
        print self.curdir
        try:
            f = open(self.curdir + "/" + self.name + ".log", "a")
            flag = 1
        except:
            try:
                f = open(self.curdir + "/" + self.name + ".log", "w")
                flag = 1
            except:
                flag = 0
        if(flag == 1):
            if self.printtooutput:
              mystr = str(time.asctime(time.localtime(time.time())) + " ---- " + str(s) + '\n')
            f.write(mystr)
            if self.printtooutput:
                print mystr
            f.close()

  def removelog(self):
		try:
			os.remove(self.curdir + "/" + self.name + ".log")
		except:
			a = 1
	
	def readlog(self):
		try:
			f = open(self.curdir + "/" + self.name + ".log", "r")
			retstr = f.read()
			f.close()
                except:
			retstr = ""
		return retstr

	def exitlog(self):
		return os.path.exists(self.curdir + "/" + self.name + ".log")
