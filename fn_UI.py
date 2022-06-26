# Класс Экран + Всякие функции для вычисления расположения интерфейсов

from kivy.base import EventLoop
from kivy import metrics
import constants

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
    sz = MinWindowSize()/constants.LevelGridColsCount
    return sz    

def TopLabelSize():
    return ExitButtonSize() * 1.2