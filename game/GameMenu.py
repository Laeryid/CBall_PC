import fn_UI
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
import logger

class GameMenu(RelativeLayout):
    button_run = ObjectProperty(None)
    button_pause = ObjectProperty(None)
    button_stop = ObjectProperty(None)
    button_resume = ObjectProperty(None)
    button_color_transparent = (0.8, 0.8, 0.8, 0.5)
    button_color_on_menu = fn_UI.button_pict_color
    menu_color = fn_UI.interface_background_color
    layout_run = ObjectProperty(None)
    layout_change = ObjectProperty(None)
    hidden_buttons = {
            "RunGameButton": False ,
            "PauseGameButton": True , 
            "StopGameButton": False ,
            "ResumeGameButton": True,
            "LayoutRun": True,
            "LayoutChange": False
    }
    vertical_window = BooleanProperty(True)

    
    def SetMenuOrientation(self, WindowSize=fn_UI.WindowSize(),menu_status_changed = 0):
        if WindowSize[0] <= WindowSize[1]:
            # vertikal window
            self.vertical_window = True
            self.pos_hint = {'bottom': 1}
            self.height = fn_UI.GameMenuWidth()
            self.width = WindowSize[0]
            self.size_hint_y = None
            self.size_hint_x = 1.0
            self.x = 0
        else:
            # horizontal window
            self.vertical_window = False
            self.pos_hint = {'right': 1}
            self.width = fn_UI.GameMenuWidth()
            self.height = WindowSize[1]
            self.size_hint_x = None
            self.size_hint_y = 1.0  
        self.LayuotChangeDraw(self.vertical_window, menu_status_changed)
        self.LayuotRunDraw(self.vertical_window)
        self.RunButtonDraw(self.vertical_window)
        self.ResumeButtonDraw(self.vertical_window)
        self.PauseButtonDraw(self.vertical_window)
        self.StopButtonDraw(self.vertical_window)

    def LayuotChangeDraw(self, vertical_window, menu_status_changed):
        if menu_status_changed == 0:
            if self.hidden_buttons["LayoutChange"]:
                if vertical_window:
                    self.layout_change.x = 0
                    self.layout_change.y = -self.height
                else:
                    self.layout_change.x = self.width
                    self.layout_change.y = 0
                return 
            self.layout_change.x = 0
            self.layout_change.y = 0
        else:
            x = 0
            y = 0
            if self.hidden_buttons["LayoutChange"]:
                if vertical_window:
                    y = -self.height
                else:
                    x = self.width
            anim = Animation(x = x, y = y, t = 'in_circ', duration = 0.2)
            anim.start(self.layout_change)
       
        
    def LayuotRunDraw(self, vertical_window):
        if self.hidden_buttons["LayoutRun"]:
            if vertical_window:
                self.layout_run.x = 0
                self.layout_run.y = -self.height
            else:
                self.layout_run.x = self.width
                self.layout_run.y = 0
            return 
        self.layout_run.x = 0
        self.layout_run.y = 0
        

    def RunButtonDraw(self, vertical_window):
        if vertical_window:
            self.button_run.x = 0
            self.button_run.y = 0
            self.button_run.size_hint_y = 1
            self.button_run.size_hint_x = 0.25           
        else:
            self.button_run.y = 0.75 * self.height
            self.button_run.x = 0
            self.button_run.size_hint_x = 1
            self.button_run.size_hint_y = 0.25
            
    def ResumeButtonDraw(self, vertical_window):
        if self.hidden_buttons["ResumeGameButton"]:
            self.button_resume.x = -100
            self.button_resume.y = -100
            self.button_resume.size_hint_y = 0.0
            self.button_resume.size_hint_x = 0.0
            return
        if vertical_window:
            self.button_resume.x = 0
            self.button_resume.y = 0
            self.button_resume.size_hint_y = 1
            self.button_resume.size_hint_x = 0.25
        else:
            self.button_resume.y = 0.75 * self.height
            self.button_resume.x = 0
            self.button_resume.size_hint_x = 1
            self.button_resume.size_hint_y = 0.25
            
    def PauseButtonDraw(self, vertical_window):
        if self.hidden_buttons["PauseGameButton"]:
            self.button_pause.x = -100
            self.button_pause.y = -100
            self.button_pause.size_hint_y = 0.0
            self.button_pause.size_hint_x = 0.0
            return
        if vertical_window:
            self.button_pause.x = 0
            self.button_pause.y = 0
            self.button_pause.size_hint_y = 1
            self.button_pause.size_hint_x = 0.25 
        else:
            self.button_pause.y = 0.75 * self.height
            self.button_pause.x = 0
            self.button_pause.size_hint_x = 1
            self.button_pause.size_hint_y = 0.25
            
    def StopButtonDraw(self, vertical_window):
        if vertical_window:
            self.button_stop.x = 0.25 * self.width
            self.button_stop.y = 0
            self.button_stop.size_hint_y = 1
            self.button_stop.size_hint_x = 0.25 
        else:
            self.button_stop.y = 0.5 * self.height
            self.button_stop.x = 0
            self.button_stop.size_hint_x = 1
            self.button_stop.size_hint_y = 0.25