import wx

class MessageBoxs():

    def __init__(self, Message,Title):
         self.Message=Message
         self.Title=Title
    
    def Error_Message_Box(self):
        self.msg = wx.MessageDialog(None, self.Message, self.Title,
        wx.OK | wx.ICON_ERROR)
        self.msg.ShowModal()
        self.msg.Destroy()

    def Info_Message_Box(self):
        self.msg = wx.MessageDialog(None, self.Message, self.Title,
            wx.OK |wx.ICON_INFORMATION)
        self.msg.ShowModal()
        self.msg.Destroy()

    def Qustion_Message_Box(self):
        self.msg=wx.MessageDialog(None, self.Message, self.Title,
           wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        return self.msg.ShowModal()
        self.msg.Destroy()
        
    def No_Button_Message_Box(self):
        self.msg=wx.MessageDialog(None, self.Message, self.Title,
           wx.ICON_INFORMATION)
        self.msg.CenterOnParent()
        self.msg.Show(True)
        self.msg.SetFocus()
        
    def Close_No_Button_Message_Box(self):
         self.msg.Close()
         self.msg.Destroy()
         
