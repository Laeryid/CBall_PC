import CBall_Screen
import fn_UI
import game.game
from kivy.properties import ObjectProperty
import logger
from kivy.base import EventLoop


class GameScr(CBall_Screen.CBall_Screen):
    game_schedule = ObjectProperty(None)
    game = ObjectProperty(None)
    game_menu = ObjectProperty(None)
    window_size = (0.0, 0.0)
    
    
    
    def __init__ (self,*args,  **kwargs):
        super(GameScr, self).__init__(*args, **kwargs)
        
       
    def RunGame(self):
        if self.game.status == 0:
            self.game.RunGame()
            logger.InsertLog('Game start')        
        if self.game.status != 1:
            self.SetGameStatus(1)
            
    def ResumeGame(self):
        if self.game.status == 2:
            self.game.ResumeGame()
            logger.InsertLog('Game restart')
        if self.game.status != 1:
            self.SetGameStatus(1)
        
            
    def PauseGame(self):           
        self.SetGameStatus(2)
        self.game.PauseGame()       
        logger.InsertLog('Game pause')
                 
                
    def StopGame(self):
        self.SetGameStatus(0)   
        self.game.StopGame()             
        logger.InsertLog('Game stop')

    def LoadGame(self):
        EventLoop.ensure_window()
        self.window_size = EventLoop.window.size
        self.game_menu.button_run.on_press = self.RunGame
        self.game_menu.button_resume.on_press = self.ResumeGame
        self.game_menu.button_pause.on_press = self.PauseGame
        self.game_menu.button_stop.on_press = self.StopGame
        self.SetGameStatus(0)
        self.game.LoadGame()
        self.game_menu.SetMenuOrientation()
        logger.InsertLog('Game loaded')
        
    def ResizeGame(self, size):
        self.window_size = size
        self.game.ResizeGame(size)
        self.game_menu.SetMenuOrientation(size)

    def SetGameStatus(self, status):
        if status == self.game.status and status != 0:
            return
        if (status == 0 or self.game.status == 0) and status != self.game.status:
            menu_status_changed = 1
        else:
            menu_status_changed = 0
        if status == 0:
            self.game_menu.hidden_buttons["ResumeGameButton"] = True
            self.game_menu.hidden_buttons["PauseGameButton"] = True
            self.game_menu.hidden_buttons["LayoutRun"] = True
            self.game_menu.hidden_buttons["LayoutChange"] = False
        if status == 1:
            self.game_menu.hidden_buttons["ResumeGameButton"] = True
            self.game_menu.hidden_buttons["PauseGameButton"] = False
            self.game_menu.hidden_buttons["LayoutRun"] = False
            self.game_menu.hidden_buttons["LayoutChange"] = True
        if status == 2:
            self.game_menu.hidden_buttons["ResumeGameButton"] = False
            self.game_menu.hidden_buttons["PauseGameButton"] = True
            self.game_menu.hidden_buttons["LayoutRun"] = False
            self.game_menu.hidden_buttons["LayoutChange"] = True
        self.game.status = status 
        self.game_menu.SetMenuOrientation(self.window_size, menu_status_changed)
