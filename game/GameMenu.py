import fn_UI
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ListProperty
import logger
from typing import Dict

class GameMenu(RelativeLayout):
#    game = ObjectProperty(None)
    button_run = ObjectProperty(None)
    button_pause = ObjectProperty(None)
    button_stop = ObjectProperty(None)
    button_resume = ObjectProperty(None)
    button_instruments_open = ObjectProperty(None)
    button_instruments_close = ObjectProperty(None)
    button_instruments_angle = NumericProperty(0)
    button_instruments_center = ListProperty((0,0))
    button_color_transparent = (0.8, 0.8, 0.8, 0.5)
    button_color_on_menu = fn_UI.button_pict_color
    menu_color = fn_UI.interface_background_color
    layout_run = ObjectProperty(None)
    layout_change = ObjectProperty(None)
    layout_instruments = ObjectProperty(None)
    hidden_buttons = {
            "RunGameButton": False ,
            "PauseGameButton": True , 
            "StopGameButton": False ,
            "ResumeGameButton": True,
            "LayoutRun": True,
            "LayoutChange": False,
            "LayoutInstruments": True
    }
    vertical_window = BooleanProperty(True)
    instruments_count = NumericProperty(1)
    instruments_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameMenu, self).__init__(**kwargs)

    def SetInstruments(self, count, instruments_dict: Dict, game):
        self.instruments_count = count
#        self.instruments_list = []
        for instr in instruments_dict["Smooth"]:
            instr.game = game
            self.instruments_list.add_widget(instr)
            
    def ClearInstruments(self):
        self.instruments_list.clear_widgets()
    
    def SetMenuOrientation(self, WindowSize=fn_UI.WindowSize(),menu_status_changed = 0, instruments_status_change = 0):
        if WindowSize[0] <= WindowSize[1]:
            # vertikal window
            self.vertical_window = True
            self.height = fn_UI.GameMenuWidth()
            self.width = WindowSize[0]
            self.x = 0
            self.button_instruments_angle = 0
            self.button_instruments_center = (0.875* self.width, 0.5*self.height)
            self.instruments_list.orientation= 'vertical'
        else:
            # horizontal window
            self.vertical_window = False
            self.width = fn_UI.GameMenuWidth()
            self.height = WindowSize[1]
            self.x = WindowSize[0] - self.width
            self.button_instruments_angle = 90
            self.button_instruments_center = (0.5* self.width, 0.125*self.height)
            self.instruments_list.orientation= 'horizontal'
        self.LayoutChangeDraw(self.vertical_window, menu_status_changed)
        self.LayoutRunDraw(self.vertical_window)
        self.LayoutInstrumentsDraw(self.vertical_window, menu_status_changed, instruments_status_change)
        self.RunButtonDraw(self.vertical_window)
        self.ResumeButtonDraw(self.vertical_window)
        self.PauseButtonDraw(self.vertical_window)
        self.StopButtonDraw(self.vertical_window)
        logger.InsertLog((self.button_instruments_close.x, self.button_instruments_close.y, self.button_instruments_center[0], self.button_instruments_center[1], self.hidden_buttons["LayoutInstruments"]))

    def LayoutChangeDraw(self, vertical_window, menu_status_changed):
        x= 0
        y = 0
        if self.hidden_buttons["LayoutChange"]:
            if vertical_window:
                y = -self.height
            else:
                x = self.width                
        if menu_status_changed == 0: 
            self.layout_change.x = x
            self.layout_change.y = y
        else:            
            anim = Animation(x = x, y = y, t = 'in_circ', duration = 0.2)
            anim.start(self.layout_change)
       
    def  LayoutInstrumentsDraw(self, vertical_window, menu_status_changed, instruments_status_change):
        if vertical_window:
            menu_width = self.height
            menu_length = self.width         
        else:
            menu_width = self.width
            menu_length = self.height                  
        instruments_width = fn_UI.GameMenuWidth()
        instruments_height = self.instruments_count*instruments_width
        instruments_across_menu = menu_width # сдвиг поперек меню, от его нижнего/правого края
        instruments_along_menu = 0 #сдвиг вдоль меню, от его правого/нижнего края
        if vertical_window:
            start_along = menu_length-instruments_width
            mult_along = -1
            start_across = 0
            mult_across = 1   
        else:
            start_along = 0
            mult_along = 1
            start_across = menu_width - instruments_height
            mult_across = -1   
                    
        if self.hidden_buttons["LayoutInstruments"]:
             instruments_across_menu = - instruments_height + menu_width
        if self.hidden_buttons["LayoutChange"]:
             instruments_across_menu = - instruments_height
        if vertical_window:
            x = start_along + mult_along*instruments_along_menu
            y = start_across + mult_across*instruments_across_menu
            self.layout_instruments.width = instruments_width
            self.layout_instruments.height = instruments_height
        else:
            x = start_across + mult_across*instruments_across_menu
            y = start_along + mult_along * instruments_along_menu
            self.layout_instruments.width = instruments_height
            self.layout_instruments.height = instruments_width

        self.InstrumentsOpenButtonDraw(vertical_window)
        self.InstrumentsCloseButtonDraw(vertical_window)
                            
        if instruments_status_change == 0 and menu_status_changed == 0:
            self.layout_instruments.x = x
            self.layout_instruments.y = y  
        else:
            anim = Animation(x = x, y = y, t = 'in_circ', duration = 0.2)
            anim.start(self.layout_instruments)
            
    def LayoutRunDraw(self, vertical_window):
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
            
    def InstrumentsOpenButtonDraw(self, vertical_window):
        if not self.hidden_buttons["LayoutInstruments"]:
            self.button_instruments_open.x = -100
            self.button_instruments_open.y = -100
            self.button_instruments_open.size_hint_y = 0.0
            self.button_instruments_open.size_hint_x = 0.0
            return
        if vertical_window:
            self.button_instruments_open.x = 0.75 * self.width
            self.button_instruments_open.y = 0
            self.button_instruments_open.size_hint_y = 1
            self.button_instruments_open.size_hint_x = 0.25 
        else:
            self.button_instruments_open.y = 0
            self.button_instruments_open.x = 0
            self.button_instruments_open.size_hint_x = 1
            self.button_instruments_open.size_hint_y = 0.25
            
    def InstrumentsCloseButtonDraw(self, vertical_window):
        if self.hidden_buttons["LayoutInstruments"]:
            self.button_instruments_close.x = -100
            self.button_instruments_close.y = -100
            self.button_instruments_close.size_hint_y = 0.0
            self.button_instruments_close.size_hint_x = 0.0
            return
        if vertical_window:
            self.button_instruments_close.x = 0.75 * self.width
            self.button_instruments_close.y = 0
            self.button_instruments_close.size_hint_y = 1
            self.button_instruments_close.size_hint_x = 0.25
        else:
            self.button_instruments_close.y = 0
            self.button_instruments_close.x = 0
            self.button_instruments_close.size_hint_x = 1
            self.button_instruments_close.size_hint_y = 0.25
            