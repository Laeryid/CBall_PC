import fn_UI
import constants
from kivy.uix.screenmanager import Screen
import logger

class CBall_Screen(Screen):
    def ExitSize(self, *args):
        return fn_UI.ExitButtonSize()
    def TopLabelSize(self, *args):
        return fn_UI.TopLabelSize()
    def LabelSize(self, *args):
        return 100
    def LevelCellSize(self, *args):
        return fn_UI.LevelCellSize_fn()
    def LevelGridColsCount(self, *args):
        return constants.LevelGridColsCount
    def GameMenuWidth(self):
        return fn_UI.GameMenuWidth()
    def GameMenuPosHint(self):
        return fn_UI.GameMenuPosHint()
    def RotateGame(self):
        logger.InsertLog('Rotated on screen ' + type(self).__name__)