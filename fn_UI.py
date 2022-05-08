# Класс Экран + Всякие функции для вычисления расположения интерфейсов

from kivy.base import EventLoop
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import metrics
import logger

LevelGridColsCount = 5

wall_types = ('Walls', # простые прямые стены
        'RWalls',  # простые круглые стены
#        'AWalls',  # углы между стенами, в которые может ударить шар
        'SSWalls',  # мягкие прямые стены
        'SRWalls',  # мягкие круглые стены
        'JSWalls',  # упругие прямые стены
)

wall_types_for_beat_calc = (
        ('JSWalls',
        'SSWalls',
        'SRWalls'
        ) ,
        ('Walls',
        'RWalls',
        'AWalls'
        )
)

interface_background_color = (0.2, 0.35, 0.5, 1)
button_pict_color = (0.8, 0.8, 0.8, 1)

def WindowSize():
    EventLoop.ensure_window()
    return EventLoop.window.size

def MinWindowSize():
    return min(WindowSize())

def ExitButtonSize():
    minsz = MinWindowSize()
    sz = minsz/10
    if sz < metrics.mm(7):
        sz = metrics.mm(7)
    return sz
    
def WindowOrientationVertical():
    WS = WindowSize()
    if WS[0] < WS[1]:
        return True
    else:
        return False
        
def GameMenuPosHint():
    if WindowOrientationVertical():
        return {'bottom' : 1}
    else:
        return {'right' : 1}
        
def GameMenuWidth():
    return MinWindowSize() / 4
    
def LevelCellSize_fn():
    sz = MinWindowSize()/LevelGridColsCount
    return sz    

def TopLabelSize():
    return ExitButtonSize() * 1.2

class CBall_Screen(Screen):
    def ExitSize(self, *args):
        return ExitButtonSize()
    def TopLabelSize(self, *args):
        return TopLabelSize()
    def LabelSize(self, *args):
        return 100
    def LevelCellSize(self, *args):
        return LevelCellSize_fn()
    def LevelGridColsCount(self, *args):
        return LevelGridColsCount
    def GameMenuWidth(self):
        return GameMenuWidth()
    def GameMenuPosHint(self):
        return GameMenuPosHint()
    def RotateGame(self):
        logger.InsertLog('Rotated on screen ' + type(self).__name__)