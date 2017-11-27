from collections import OrderedDict

import clr
clr.AddReference("Eto")
from Eto.Forms import Form,Panel,Dialog, Label, TabControl,ComboBox, TabPage, TextBox, TextArea,StackLayout,StackLayoutItem, Orientation, Button,HorizontalAlignment, MessageBox
from Eto.Drawing import *

import rsTools
reload(rsTools)
from rsTools import *


import RsTools.FormMorph as rtf
reload(rtf)

class FormEditParam(Form):
    def __init__(self):
        self.param_obj=None
        self.size=Size(200,500)
        layV = StackLayout(Spacing=2, Orientation=Orientation.Vertical)
        self.lay_comps = StackLayout(Spacing=2, Orientation=Orientation.Vertical)
        layV.Items.Add(self.lay_comps)
        bt_confirm=Button()
        bt_confirm.Text='Confirm'
        layV.Items.Add(bt_confirm)
        self.Content=layV
        self.bt_confirm=bt_confirm

    def set_param_obj(self,param_obj):
        self.param_obj=param_obj
        texts={}
        for key, value in param_obj.items():
            print(key,value)
            layH = StackLayout(Spacing=2, Orientation=Orientation.Horizontal)
            title = Label()
            title.Text=key
            title.Size = Size(100, 20)
            txtbox = TextBox()
            txtbox.Text=str(value)
            txtbox.Size = Size(100, 20)
            texts[key]=txtbox

            layH.Items.Add(title)
            layH.Items.Add(txtbox)
            self.lay_comps.Items.Add(layH)

        def handle_click(sender,e):
            for key in texts:
                txtbox=texts[key]
                try:
                    value=txtbox.Text
                    print(self.param_obj,title.Text,value)
                    self.param_obj[key]=float(value)
                except Exception as e:
                    print(e)
            print('------------------')
            print(self.param_obj)
            self.on_param_update(self.param_obj)

        self.bt_confirm.Click += handle_click
        return texts

    def on_param_update(self, param):
        #override this methos
        pass


class ShapeBase():
    def __init__(self):
        self.box=None
        self.form=None
        self.param=None
        self.set_param()

    def show_params(self):
        if self.form is None:
            return
        self.form.Show()

    def set_box(self, brepid):
        self.box=brepid
        self.form=FormEditParam()
        self.form.set_param_obj(self.param)
        self.form.on_param_update=self.update

    def set_param(self,param={}):
        self.param = OrderedDict({'w1': 0.4, 'w2': 0.5, 'w3': 0.1})

    def update(self,param=None):
        if param is None:
            param=self.param
        sel = rs.ObjectsByName('generated')
        try:
            rs.DeleteObjects(sel)
        except:
            pass
        self.on_update(param)
        #update method
        #override this method
        pass

    def on_update(self):
        #override
        pass

class Shape1():
    def set_param(self):
        self.param = OrderedDict({'w1': 0.4, 'w2': 0.5, 'w3': 0.1})
    def on_update(self, param):
        flag, orgvect = rtf.is_solid_box(self.box)
        v1 = orgvect[1] * 0.2
        w1 = param['w1']
        w2 = param['w2']
        w2 = param['w3']
        values = list(param.values())
        rs.EnableRedraw(False)
        comps = rtf.box_div_h(self.box, values)
        for comp in comps:
            rs.ObjectName(comp, 'generated')
        rs.MoveObject(comps[0], v1)
        rs.MoveObject(comps[1], -v1)
        rs.HideObject(self.box)
        rs.EnableRedraw(True)