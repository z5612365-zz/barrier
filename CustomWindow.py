from PySide2 import QtWidgets
from BaseUI import MUIWindow
import maya.cmds as cmds


class CustomWindow(MUIWindow.MUIWindow):

    def __init__(self):
        ui_url = '/home/chi/maya/scripts/MUI/resource/mui.ui'
        super(CustomWindow,self).__init__(ui_url)

    # ----------------------------------------------- init UI stuff -----------------------------------------------
    def init_UI(self):
        self.btn = self.getUIElement(QtWidgets.QPushButton,"pushButton")
        self.lineEdit = self.getUIElement(QtWidgets.QLineEdit,"lineEdit")
        self.label = self.getUIElement(QtWidgets.QLabel,"label")

        self.text=self.lineEdit.text()

    def updateValue(self):

        self.btn.clicked.connect(self.updateMainValue)

    def SignalSlotLinker(self):
        self.btn.clicked.connect( self.updateLineEdit)
        self.btn.clicked.connect( self.CreateObjects)
        self.btn.clicked.connect( self.AnimeObjects)


    def updateMainValue(self):
        self.text = self.lineEdit.text()


    def updateLineEdit(self):
        self.label.setText(self.text)

    # ----------------------------------------------- slot function -----------------------------------------------


    def CreateObjects(self):
        SphereRadius=1

        cmds.polySphere(n='Sphere', sx=10, sy=10, r=SphereRadius)
        cmds.polySphere(n='SpherePin', sx=10, sy=10, r=SphereRadius)
        cmds.setAttr('Sphere.translateY', 6)
        cmds.setAttr('Sphere.translateZ', 8)


        cmds.constrain( 'Sphere', 'SpherePin', pin=True, i=True, n='pin')

        cmds.constrain( 'SpherePin', nail=True, n='nail')
        cmds.select(clear=True)
        newtonfield = cmds.newton(m=1000.0)
        cmds.connectDynamic( 'Sphere', f=newtonfield[0] )


        cmds.select(clear=True)
        dragfield = cmds.drag( m=10.0 )
        cmds.connectDynamic('Sphere', f=dragfield)

        #setting
        cmds.setAttr(newtonfield[0]+'.volumeShape', 2) #set volume shape to sphere
        cmds.select(newtonfield[0])
        ouside_sphere_radius=10
        cmds.scale(ouside_sphere_radius+SphereRadius, ouside_sphere_radius+SphereRadius, ouside_sphere_radius+SphereRadius)

        cmds.setAttr(dragfield[0]+'.volumeShape', 2) #set volume shape to sphere
        cmds.select(dragfield[0])
        ouside_sphere_radius=10
        cmds.scale(ouside_sphere_radius+SphereRadius, ouside_sphere_radius+SphereRadius, ouside_sphere_radius+SphereRadius)


        #group
        cubelist = [newtonfield[0], dragfield[0], u'nail']
        print(cubelist)
        cmds.group(cubelist, n='GroupAnime')


        cubelist = [u'Sphere', u'SpherePin', u'pin', u'GroupAnime']
        print(cubelist)
        cmds.group(cubelist, n='barrier')

    def AnimeObjects(self):


        cmds.setKeyframe('GroupAnime', attribute='translateZ', t=['1'])
        cmds.setAttr('GroupAnime.translateZ', -80)
        cmds.setKeyframe('GroupAnime', attribute='translateZ', t=['20'])
        cmds.currentTime(1)


"""
newton -pos 0 0 0 -m 5 -att 1 -mnd 0.2  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;
// Result: newtonField2 // 
connectDynamic -f newtonField2  Sphere;
// Result: rigidBody6 // 


drag -pos 0 0 0 -m 0.05 -att 1 -dx 0 -dy 0 -dz 0 -ud 0  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;
// Result: dragField1 // 
connectDynamic -f dragField1  Sphere;
// Result: rigidBody1 // 


setAttr "newtonField1.volumeShape" 2;
select -r newtonField1 ;
selectKey -clear ;
// Result: 0 // 
scale -ws -r 11.183333 11.183333 11.183333 ;
"""
