
import sys
from SerialPorts import *
from Event import Event
from MessageBoxs import *
import wx
import time
from Log import *

class ATDialSpeechModem():
   

    def __init__(self, port,Baudrate,initializeAT,CallerIDAT):
       self._SerialPorts=SerialPorts(port,Baudrate)
       self.Log=Logs()
       if self._SerialPorts.Get_IsOpen :
            
            #print self._SerialPorts.write('AT&F \r','OK')#reset factory
            self._SerialPorts.write('ATZ \r\n','OK',2)#rese
            self._SerialPorts.write(initializeAT +'\r\n','OK')#reset
            print self._SerialPorts.write(CallerIDAT+'\r\n','OK')#caller id
            
            self._SerialPorts.readavailable += self.OnReadAvailable
            self._SerialPorts.start()
            self.Readline=""
            self.time_previuseevent=time.time()
           
    
    #@anythread
    def FireMessageBox(self):
        try:
            #Not working yet **************************************************************
            #self.MyMessageBox=MessageBoxs(self.Readline,'Info')
            #self.MyMessageBox.Info_Message_Box()
            #dial = wx.MessageDialog(None, self.Readline, "Info", wx.OK |wx.ICON_INFORMATION)
            #dial.ShowModal()
            #************************************************************** Not working yet
            self.Log.writelog( " *************************************" + self.Readline)
        except Exception as ex:
            self.Log.writelog("FireMessageBox %s" % str(ex))

    def OnReadAvailable(self,Readline):
        try:
            if self.Readline!=Readline:
                self.Readline=Readline
                self.time_previuseevent=time.time()
                self.FireMessageBox()
            else:
                if self.time_previuseevent+60<time.time():
                    self.Readline=Readline
                    self.time_previuseevent=time.time()
                    self.FireMessageBox()
        except Exception as ex:
            self.Log.writelog("OnReadAvailable %s" % str(ex))

    def __finalize__(self):
           self._SerialPorts.stop()

    def Dial(self,PhoneNumber):
        #PhoneNumber=str(PhoneNumber).replace('+', '00')
        self._SerialPorts.Set_Write_Lines('ATD ' + PhoneNumber + ';H\r\n')

    def HangUp(self):
        self._SerialPorts.Set_Write_Lines('ATH \r\n')
    
    def Test(self):
        self._SerialPorts.Set_Write_Lines('AT \n')
       

    
