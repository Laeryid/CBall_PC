import fn_UI
import constants
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ListProperty
import logger

class GameMenu(RelativeLayout):
    button_run = ObjectProperty(None)
    button_pause = ObjectProperty(None)
    button_stop = ObjectProperty(None)
    button_resume = ObjectProperty(None)
    button_elem_list = ObjectProperty(None)
    active_elements_list_button_texture = ListProperty([])
    button_color_transparent = (0.8, 0.8, 0.8, 0.5)
    button_color_on_menu = constants.button_pict_color
    menu_buttons_lines_width = NumericProperty(20)
    menu_color = constants.interface_background_color
    layout_run = ObjectProperty(None)
    layout_change = ObjectProperty(None)
    layout_elem_list = ObjectProperty(None)
    elem_count = NumericProperty(0)
    hidden_buttons = {
            "RunGameButton": False ,
            "PauseGameButton": True , 
            "StopGameButton": False ,
            "ResumeGameButton": True ,
            "ElemListButton": False ,
            "LayoutRun": True ,
            "LayoutChange": False,
            "LayoutElemList": True
    }
    vertical_window = BooleanProperty(True)
    elem_list_is_opened = BooleanProperty(False)
    menu_proportions = NumericProperty(fn_UI.GameMenuProportions())


    
    def SetMenuOrientation(self, WindowSize=fn_UI.WindowSize(),menu_status_changed = 0):
        GameMenuWidth = fn_UI.GameMenuWidth()
        if WindowSize[0] <= WindowSize[1]:
            # vertikal window
            self.vertical_window = True
            self.pos_hint = {'bottom': 1}
            self.height = GameMenuWidth
            self.width = WindowSize[0]
            self.size_hint_y = None
            self.size_hint_x = 1.0
            self.x = 0
            self.layout_elem_list.width = GameMenuWidth
            self.layout_elem_list.height = GameMenuWidth * self.elem_count
        else:
            # horizontal window
            self.vertical_window = False
            self.pos_hint = {'right': 1}
            self.width = GameMenuWidth
            self.height = WindowSize[1]
            self.size_hint_x = None
            self.size_hint_y = 1.0
            self.layout_elem_list.height = GameMenuWidth
            self.layout_elem_list.width = GameMenuWidth * self.elem_count
        self.menu_buttons_lines_width = GameMenuWidth * 0.15
        self.menu_proportions = fn_UI.GameMenuProportions()
        self.active_elements_list_button_texture = self.ElemListButtonTexture(self.vertical_window)
        self.LayuotChangeDraw(self.vertical_window, menu_status_changed)
        self.LayuotRunDraw(self.vertical_window)
        self.RunButtonDraw(self.vertical_window)
        self.ResumeButtonDraw(self.vertical_window)
        self.PauseButtonDraw(self.vertical_window)
        self.StopButtonDraw(self.vertical_window)
        self.ElemListButtonDraw(self.vertical_window)

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
            self.button_run.size_hint_x = self.menu_proportions
        else:
            self.button_run.size_hint_x = 1
            self.button_run.size_hint_y = self.menu_proportions
            self.button_run.y = self.height * (1 - self.menu_proportions)
            self.button_run.x = 0
        logger.InsertLog("Draw Run button")
            
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
            self.button_resume.size_hint_x = self.menu_proportions
        else:
            self.button_resume.y = (1 - self.menu_proportions) * self.height
            self.button_resume.x = 0
            self.button_resume.size_hint_x = 1
            self.button_resume.size_hint_y = self.menu_proportions
            
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
            self.button_pause.size_hint_x = self.menu_proportions
        else:
            self.button_pause.y = (1 - self.menu_proportions) * self.height
            self.button_pause.x = 0
            self.button_pause.size_hint_x = 1
            self.button_pause.size_hint_y = self.menu_proportions
            
    def StopButtonDraw(self, vertical_window):
        if vertical_window:
            self.button_stop.x = (1 - self.menu_proportions) * self.width
            self.button_stop.y = 0
            self.button_stop.size_hint_y = 1
            self.button_stop.size_hint_x = self.menu_proportions
        else:
            self.button_stop.y = 2 * self.menu_proportions * self.height
            self.button_stop.x = 0
            self.button_stop.size_hint_x = 1
            self.button_stop.size_hint_y = self.menu_proportions

    def ElemListButtonTexture(self, vertical_window):
        if vertical_window:
            return [
                self.button_elem_list.x + 0.2 * self.width * self.menu_proportions
                , self.button_elem_list.y + (0.5 - 0.15 * (1 - 2 * self.elem_list_is_opened)) * self.height
                , self.button_elem_list.x + 0.5 * self.width * self.menu_proportions
                , self.button_elem_list.y + (0.5 + 0.15 * (1 - 2 * self.elem_list_is_opened)) * self.height
                , self.button_elem_list.x + 0.8 * self.width * self.menu_proportions
                , self.button_elem_list.y + (0.5 - 0.15 * (1 - 2 * self.elem_list_is_opened)) * self.height
            ]
        else:
            return [
                self.button_elem_list.x + (0.5 + 0.15 * (1 - 2 * self.elem_list_is_opened)) * self.width
                , self.button_elem_list.y + 0.2 * self.height * self.menu_proportions
                , self.button_elem_list.x + (0.5 - 0.15 * (1 - 2 * self.elem_list_is_opened)) * self.width
                , self.button_elem_list.y + 0.5 * self.height * self.menu_proportions
                , self.button_elem_list.x + (0.5 + 0.15 * (1 - 2 * self.elem_list_is_opened)) * self.width
                , self.button_elem_list.y + 0.8 * self.height * self.menu_proportions
            ]

    def ElemListButtonDraw(self, vertical_window):
        if vertical_window:
            self.button_elem_list.x = (1 - self.menu_proportions) * self.width
            self.button_elem_list.y = 0
            self.button_elem_list.size_hint_y = 1
            self.button_elem_list.size_hint_x = self.menu_proportions
        else:
            self.button_elem_list.y = 0
            self.button_elem_list.x = 0
            self.button_elem_list.size_hint_x = 1
            self.button_elem_list.size_hint_y = self.menu_proportions
        self.active_elements_list_button_texture = self.ElemListButtonTexture(vertical_window)
        logger.InsertLog("Draw ElemList button")

    def ElemListChangeStatus(self):
        self.elem_list_is_opened = not(self.elem_list_is_opened)
        logger.InsertLog("self.elem_list_is_opened: {}".format(self.elem_list_is_opened))
        self.ElemListButtonDraw(self.vertical_window)
        self.hidden_buttons['LayoutElemList'] = not(self.elem_list_is_opened)
        self.LayoutElemListDraw(self.vertical_window)

    def LayoutElemListDraw(self, vertical_window):
        GameMenuWidth = fn_UI.GameMenuWidth()
        if (self.hidden_buttons["LayoutElemList"]) or not(self.elem_list_is_opened):
            if vertical_window:
                x = self.width - GameMenuWidth
                y = - GameMenuWidth * self.elem_count
            else:
                x = self.width
                y = 0
        else:
            if vertical_window:
                x = self.width - GameMenuWidth
                y = self.height
            else:
                x = - GameMenuWidth * self.elem_count
                y = 0
        anim = Animation(x = x, y = y, t = 'in_circ', duration = 0.2)
        anim.start(self.layout_elem_list)
        logger.InsertLog("self.hidden_buttons[''LayoutElemList'']: {}, self.elem_list_is_opened: {}".format(
                            self.hidden_buttons["LayoutElemList"]
                            , self.elem_list_is_opened))
        logger.InsertLog("x: {}, y: {}".format(x, y))