import wx
import re

import matplotlib.pyplot as plt


class Example(wx.Frame):
    oldx=[]
    red = 1
    green = 1
    blue = 1
    red2 = 0
    green2 = 0
    blue2 = 1
    oldy=[]
    x=[]
    y=[]
    RadialActivated = False
    contentSaved = False
    
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):

        pnl = wx.Panel(self)
       
        AddButton = wx.Button(pnl, label='Add', pos=(450, 25))
        removeButton = wx.Button(pnl, label='Remove Selected', pos=(450, 100))
        modifyButton = wx.Button(pnl, label='Modify Selected', pos=(450, 140))
       
        wx.StaticBox(pnl, label='Mode', pos=(5, 5), size=(150, 75))
        linear =wx.RadioButton(pnl, label='Linear', pos=(15, 30))
        radial=wx.RadioButton(pnl, label='Radial', pos=(75, 30))
        wx.StaticText(pnl, label='add new pair', pos=(200, 25))
        self.txtCTRL =wx.TextCtrl(pnl,pos=(300,25))
        wx.StaticBox(pnl, label='Graph Option', pos=(5, 90), size=(150, 130))
        xaxis=wx.CheckBox(pnl, label='X (angle) axis', pos=(15, 105))
        yaxis=wx.CheckBox(pnl, label='Y (Offset) axis', pos=(15, 125))
        wx.StaticText(pnl, label='Background Color', pos=(15, 165))
        linear.SetValue(True)
        wx.StaticText(pnl, label='Graph color', pos=(15, 185))
        BuildGraphButton = wx.Button(pnl, label='Build Graph', pos=(15, 230))
        moveUpButton = wx.Button(pnl, label='Move Up', pos=(450, 275))
        moveDownButton = wx.Button(pnl, label='Move Down', pos=(450,310 ))
        self.color_picker = wx.ColourPickerCtrl(pnl,size = (30,20), pos=(120,165))
        self.color_picker.SetColour((255,255,255))
        self.Bind(wx.EVT_COLOURPICKER_CHANGED,self.OnWhite, id = self.color_picker.GetId())
        self.color_picker2 = wx.ColourPickerCtrl(pnl,size = (30,20), pos=(120,185))
        self.color_picker2.SetColour((0,0,255))
        
        self.Bind(wx.EVT_COLOURPICKER_CHANGED,self.OnBlue,id = self.color_picker2.GetId())
        wx.StaticBox(pnl, label='Datasource', pos=(190, 5), size=(380, 340))
        self.listbox = wx.CheckListBox(pnl,pos=(200,100),size = (200,200))
        self.Bind(wx.EVT_RADIOBUTTON,self.OnRadial,id = radial.GetId())
        self.Bind(wx.EVT_RADIOBUTTON,self.OnLinear,id = linear.GetId())
        

        self.Bind(wx.EVT_BUTTON,self.NewItem,id = AddButton.GetId())    
        self.Bind(wx.EVT_BUTTON,self.OnDelete,id = removeButton.GetId()) 
        self.Bind(wx.EVT_BUTTON,self.OnModify,id = modifyButton.GetId())
        self.Bind(wx.EVT_BUTTON,self.OnGraph,id = BuildGraphButton.GetId())
        self.Bind(wx.EVT_BUTTON,self.OnMoveUp,id = moveUpButton.GetId())
        self.Bind(wx.EVT_BUTTON,self.OnMoveDown,id = moveDownButton.GetId())
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        open = fileMenu.Append(wx.ID_OPEN,'&Open')
        save = fileMenu.Append(wx.ID_SAVE, '&Save')
        close = fileItem = fileMenu.Append(wx.ID_EXIT, 'Close', 'Quit application')
        EditMenu = wx.Menu()
        undo = EditMenu.Append(wx.ID_UNDO, '&Undo')
        find = EditMenu.Append(wx.ID_FIND, '&Find')
        AboutMenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnOpen, open)
        self.Bind(wx.EVT_MENU, self.OnSave, save)
        self.Bind(wx.EVT_MENU, self.OnClose, close)
        self.Bind(wx.EVT_MENU, self.OnUndo, undo)
        self.Bind(wx.EVT_MENU, self.OnFind, find)

        
        fileMenu.AppendSeparator()
        menubar.Append(fileMenu, '&File')
        menubar.Append(EditMenu, '&Edit')
        menubar.Append(AboutMenu, '&About')
        about = AboutMenu.Append(wx.ID_ABOUT,'&About..')
        self.Bind(wx.EVT_MENU, self.OnAbout, about)
        self.SetMenuBar(menubar)


        self.SetSize((600, 400))
        self.SetTitle('wx.Button')
        self.Centre()
    def OnWhite(self,e):
        background2 = self.color_picker.GetColour()
        cnt = 0
        for i in background2:
            i = i / 255.0
            if cnt == 0:
                self.red =i;
            elif cnt == 1:
                self.green = i
            elif cnt == 2:
                self.blue = i
            cnt += 1
            

    def OnBlue(self,e):
        temp = self.color_picker2.GetColour()
        cnt = 0
        for i in temp:
            i = i / 255.0
            if cnt == 0:
                self.red2 =i;
            elif cnt == 1:
                self.green2 = i
            elif cnt == 2:
                self.blue2 = i
            cnt += 1
            
    
    
    def OnAbout(self , e):
        dialog  =wx.MessageDialog(self,"This program has been created in 4/11/2020 by Ammar-Ali as the third task for the subject software system testing ITMO University")
        dialog.SetHelpLabel("Info")
        dialog.ShowModal()
    def OnFind(self, e):
        text = wx.GetTextFromUser('Find')
        self.listbox.SetSelection(self.listbox.FindString(text))
        
    def OnUndo(self, e):
        self.x = self.oldx
        self.y = self.oldy
        self.listbox.Clear()
        for i in range(len(self.x)):
            self.listbox.Append('[' + str(self.x[i])+']X[' + str(self.y[i]) + ']' +'\n')

    def doSaveData(self , file):
        for i in range(len(self.x)):
            file.write('[' + str(self.x[i])+']X[' + str(self.y[i]) + ']' +'\n')
    def OnSave(self, event):     
        with wx.FileDialog(self, "Save txt file", wildcard="TXT files (*.txt)|*.TXT",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file)
                    self.contentSaved = True
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)


    def LoadData(self,file):
        self.x.clear()
        self.y.clear()
        self.listbox.Clear()
        for line in file:
            if self.checkInput(line,False,-1) == True:
                self.listbox.Append(line)
            else:
                dialog = wx.MessageDialog(self,
				"Invalid Input", 'Error',
				wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()

    def OnOpen(self, event):

        if self.contentSaved == False:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open TXT file", wildcard="TXT files (*.txt)|*.TXT",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.LoadData(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)


    def OnClose(self, e):
        self.Close(True)

    def OnMoveUp(self, e):
        id = self.listbox.GetSelection();
        self.listbox.SetSelection(max(id-1,0))

    def OnMoveDown(self, e):
        id = self.listbox.GetSelection();
        self.listbox.SetSelection(min(id+1,int(self.listbox.GetCount())-1))

    def OnGraph(self, e):
        fig1=plt.figure(1)
        
        ax1 = fig1.add_subplot(111)
        
        ax1.set_facecolor((self.red,self.green,self.blue))
        if self.RadialActivated == False:
            ax1.set_xlabel('X axis')
        else:
            ax1.set_xlabel('Angle')
        if self.RadialActivated == False:
            ax1.set_ylabel('Y axis')
        else:
            ax1.set_ylabel('Offset') 
        
        plt.plot(self.x,self.y,color = (self.red2,self.green2,self.blue2))
        plt.show()


    def OnRadial(self, e):
        self.RadialActivated = True


    def OnLinear(self, e):
        self.RadialActivated = False
          
        
    def NewItem(self, event):
        self.oldx.clear();
        self.oldy.clear();
        for i in range(len(self.x)):
            self.oldx.append(self.x[i])
            self.oldy.append(self.y[i])
        text = self.txtCTRL.GetValue()
        if text != '':
            if self.checkInput(text,False,-1) == True:
                self.listbox.Append(text)
            else:
                dialog = wx.MessageDialog(self,
				"Invalid Input", 'Error',
				wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()
        self.txtCTRL.Clear()


    def OnDelete(self, event):
        self.oldx.clear();
        self.oldy.clear();
        for i in range(len(self.x)):
            self.oldx.append(self.x[i])
            self.oldy.append(self.y[i])
        arr = self.listbox.GetCheckedItems()
        N = self.listbox.GetCount();
        cnt = 0
        for i in arr:
                self.x.remove(self.x[i-cnt])
                self.y.remove(self.y[i-cnt])
                cnt+=1
        self.listbox.Clear()
        for i in range(len(self.x)):
            self.listbox.Append('[' + str(self.x[i])+']X[' + str(self.y[i]) + ']' +'\n')
                
                

    def OnModify(self, event):
        self.oldx.clear();
        self.oldy.clear();
        for i in range(len(self.x)):
            self.oldx.append(self.x[i])
            self.oldy.append(self.y[i])
        arr = self.listbox.GetCheckedItems()      
        for i in arr:
            text = wx.GetTextFromUser('Modified')
            if self.checkInput(text,True,i) == True:
                self.listbox.Delete(i)
                self.listbox.Insert(text,i)
            else:
                dialog = wx.MessageDialog(self,
				"Unable To Modify Invalid Input", 'Error',
				wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()

 


    def checkInput(self, text,ok,ind):
        matched = re.match(r'\[(.+)\]X\[(.+)\]',text)
        if matched == None:
            return False
        first,second = matched.groups()
        if int(first) > 1000 or int(first) < 0 or int(second) > 1000 or int(second) < 0:
            return False
        if self.RadialActivated and first > 90:
            return False
        if ok == True:
            self.x[ind] =first
            self.y[ind] = second
        else :
            self.x.append(first)
            self.y.append(second)
        return True
           
                


            


def main():

    app = wx.App(redirect=False)
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()  