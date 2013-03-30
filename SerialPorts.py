import serial
import threading
from Event import Event
from time import *
from Log import *


class SerialPorts(object):
    def __init__(self, port, Baudrate):
        self.IsOpen=False
        self.Log=Logs()
        try:
            self.myserial = serial.Serial(port,
                baudrate=Baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False,
                writeTimeout=2
                )
            self.myserial.open()
            self.IsOpen=True
        except Exception as ex:
           self.Log.writelog("SerialPorts %s" % str(ex))
        self.Read_Lines = []
        self.Write_Lines = ""
        self.readavailable = Event()
        self.alive = False

    def Get_IsOpen(self):
        return  self.IsOpen

    def __finalize__(self):
          self.alive=False
          self.Log.writelog("Close Serial")
          self.myserial.Close()
          self.IsOpen=False


    def Get_Read_Lines(self):
        return self.Read_Lines

    def Set_Write_Lines(self,_Write_Lines):
        self.Write_Lines=_Write_Lines

    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        # start serial->console thread
        self.receiver_thread = threading.Thread(target=self.reader)
        self.receiver_thread.setDaemon(True)
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        self.receiver_thread.join()


    def start(self):

        self.alive = True
        self._start_reader()
        # enter console->serial loop
        self.transmitter_thread = threading.Thread(target=self.writer)
        self.transmitter_thread.setDaemon(True)
        self.transmitter_thread.start()

    def stop(self):
        self.alive = False
        self._stop_reader()
        
    def join(self, transmit_only=False):
        self.transmitter_thread.join()
        if not transmit_only:
            self.receiver_thread.join()

    def reader(self):
        readline=""
        #print "reader begin"
        try:
            while self.alive and self._reader_alive:
                tdata=self.myserial.readline()
                if tdata:
                    self.readavailable(tdata)
        except serial.SerialException, e:
            self.Log.writelog( "readerr Error %s" % str(e) )
            self.alive = False
            raise

    def write(self, SendStr, Result, maxcount=3):
        if self.IsOpen:
            try:
                self.myserial.write(str(SendStr))
                self.Log.writelog( str(SendStr))
                res = self.myserial.readline()
                count = 0
                while  not Result in res and count < maxcount:
                    res += self.myserial.readline()
                    count += 1
                return  res
            except Exception as ex:
                self.Log.writelog( "write %s" % str(ex) )
                self.alive = False
                return ""


    def writer(self):
        try:
            while self.alive:
                if self.Write_Lines:
                    self.myserial.write(self.Write_Lines)
                    self.Log.writelog( "writer " + self.Write_Lines)
                    self.Write_Lines=""
        except:
            self.alive = False
            self.Log.writelog( "Close writer")
            raise

