from . import loadUiWidget
from abc import ABCMeta, abstractmethod

class MUIWindow():
    __metaclass__ = ABCMeta
    def __init__(self, ui_url):
        self.MainWindow = loadUiWidget.loadUiWidget().loadUiWidget(ui_url)
        self.init_UI()
        self.SignalSlotLinker()

    # ----------------------------------------------- run -----------------------------------------------
    def run(self):
        self.MainWindow.show()

    # ----------------------------------------------- get func -----------------------------------------------
    def getUIElement(self, type, element):
        return self.MainWindow.findChild(type, element)

    # ----------------------------------------------- init UI stuff -----------------------------------------------
    @abstractmethod
    def init_UI(self):
        pass

    @abstractmethod
    def updateValue(self):
        pass

    @abstractmethod
    def SignalSlotLinker(self):
        pass
