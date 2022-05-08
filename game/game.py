import fn_UI
import game.Ball as ball_mech
import game.mechanics as game_mech
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, ReferenceListProperty, BooleanProperty
from kivy.uix.scatter import Scatter
from kivy.base import EventLoop
import game.GameMap as GM
import logger
from math import floor


class Game(Scatter):
    CBall  = ObjectProperty(None) # Главный шар
    Figure = ObjectProperty(None) # Выставляемый инструмент
    GameMap = ObjectProperty(None) # Карта уровня
    life_time = NumericProperty(None) # Длительность уровня
    # Сдвиг карты относительно окна
    game_window_x = NumericProperty(0)
    game_window_y = NumericProperty(0)
    game_window = ReferenceListProperty(game_window_x, game_window_y)
    game_window_size = ListProperty((0,0)) # Размер окна
    vertical_window = BooleanProperty(True) # Признак, что экран вертикальный
    # Размер карты уровня
    game_map_width = NumericProperty(0)
    game_map_height = NumericProperty(0)
    game_map_size = ReferenceListProperty(game_map_width, game_map_height)
    # Расположение карты относительно начала области игры (начала координат карты уровня)
    game_map_pos = ListProperty((0,0))
    small_game_map = ListProperty((0,0,0,0)) # карта маленькая в обычном режиме, карта маленькая в режиме перетаскивания
    game_menu_width = NumericProperty(0)
    # предел приращения угловой скорости
    avcmv = game_mech.angle_velocity_convertation_max_value
    status = NumericProperty(0) # статус игры
    last_second_frames = NumericProperty(0) # FPS актуальный
    scale_min = NumericProperty(0) # Минимальный масштаб
    instrument_taken = False # Признак, размещаем ли сейчас инструмент
    figure = ObjectProperty(None) # фигура, выставляемая игроком в данный момент
    game_map_history = []
    game_map_aktual_version = 0 # 0 - initial
    figure_history = []
    
    # словарь статусов игры
    game_status_dict = {
            0: "Loaded"     ,
            1: "Executing" ,
            2: "Pause"
            }
            
    # Обработчики событий
       
    def on_touch_move(self, touch):
        if self.instrument_taken:
            return True
        res = super(Game, self).on_touch_move(touch)
        self.game_window_x = self.CheckWindowX(self.pos[0], self.game_menu_width, 1)
        self.game_window_y = self.CheckWindowY(self.pos[1], self.game_menu_width, 1)
        if self.game_window_x != self.pos[0] or self.game_window_y != self.pos[1]:
            logger.InsertLog((self.pos[0], self.game_window_x)) 
            self.pos = self.game_window            
        if self.scale < self.scale_min:
            self.scale = self.scale_min
        self.CheckIsMapSmall()
        return res
 
    # функционал фигур
    
    def AddFigure(self, instrument, pos):
        new_figure = instrument.GiveFigure(pos)
        if new_figure is not None:
            self.figure = new_figure
            self.figure_history.append(instrument)
            self.add_widget(self.figure)
            
    def MoveFigure(self, pos):
        self.figure.move_to(pos)          
    
    def ReleaseFigure(self):
        self.game_map_history.append(self.GameMap.SaveLevel())
        self.game_map_aktual_version += 1
        
    def RestorePrevVersion(self):
        self.game_map_history.pop() # удаляем последнюю добавленную версию
        self.game_map_aktual_version -= 1
        self.GameMap.RestoreLevel(self.game_map_history[self.game_map_aktual_version])
        return self.figure_history.pop()
                
    # игровой функционал
    
    def CalcFPS(self, dt):
        seconds_check = self.life_time - floor(self.life_time)
        if seconds_check + dt > 1.0:
            # секунда накопилась            
            self.CBall.WriteInCenter(self.last_second_frames)
            self.last_second_frames = 0
        self.last_second_frames += 1

    def WallBeatCalculate(self, wall, dt, ball_point, ball_radius, on_surface):
        move_coeff = 1
        if wall.is_appropriate(dt, self.CBall):
            Distance = wall.PointDistance(ball_point)
            normal_vel_abs= wall.NormalVelocity(self.CBall)
            if not Distance is None and abs(Distance - ball_radius)<= 1.0 and abs(normal_vel_abs*dt) <= 1.0:
                # шар на поверхности, а не в воздухе
                on_surface =1
            if not Distance is None and Distance <= ball_radius:
                # Есть столкновение
                prev_distance = wall.PointDistance(self.CBall.center)
                if prev_distance is None:
                    prev_distance = 0
                if prev_distance-Distance>0:
                    move_coeff = (ball_radius-Distance)/(prev_distance-Distance)
                self.CBall.MoveBall(self.CBall.NextPos(dt*(1-move_coeff)))                    
                tangent_vel_abs = wall.TangentVelocity(self.CBall)
                tangent_vel_strike_loose = 0
                if self.CBall.on_surface == 1:
                    if abs(tangent_vel_abs*(1.0-wall.friction_coeff)) >= wall.friction_abs*dt:
                        friction_abs = wall.friction_abs*tangent_vel_abs/abs(tangent_vel_abs)*dt
                    else: 
                         tangent_vel_abs = 0
                         friction_abs = 0
                else:
                    friction_abs = 0
                    tangent_vel_strike_loose = tangent_vel_abs * wall.tangent_vel_loosing
                ball_a_vel = self.CBall.angle_velocity - tangent_vel_abs
                tangent_vel_from_rotation = 0
                if abs(ball_a_vel) >= self.avcmv * (1+game_mech.angle_velocity_convertation_coeff):
                    self.CBall.angle_velocity -= self.avcmv * ball_a_vel/abs(ball_a_vel)
                    tangent_vel_from_rotation = self.avcmv * ball_a_vel/abs(ball_a_vel) * game_mech.angle_velocity_convertation_coeff # коэффициент между кин. энергией поступ и вращ движ
                else:
                    self.CBall.angle_velocity -= ball_a_vel / (1+game_mech.angle_velocity_convertation_coeff)
                    tangent_vel_from_rotation = ball_a_vel * game_mech.angle_velocity_convertation_coeff / (1+game_mech.angle_velocity_convertation_coeff)                     
                if abs(normal_vel_abs*self.CBall.resiliencecoeff*wall.resiliencecoeff) < 3 and self.CBall.on_surface == 1:
                    normal_vel_abs = 0
                else:
                    normal_vel_abs = normal_vel_abs*self.CBall.resiliencecoeff*wall.resiliencecoeff
                self.CBall.velocity = game_mech.AddVector(wall.TangentVec(self.CBall.center), wall.NormalVec(self.CBall.center), tangent_vel_abs*(1.0-wall.friction_coeff)-friction_abs + tangent_vel_from_rotation - tangent_vel_strike_loose, - normal_vel_abs)
                ball_point = self.CBall.NextPos(dt*move_coeff)
        return (ball_point, on_surface)              

    def MoveGame(self, dt):
        if self.status != 1:
            return False
        self.CalcFPS(dt)
        move_coeff = 1.0
        self.life_time += dt
        ball_point = self.CBall.NextPos(dt)
        ball_radius = self.CBall.radius
        GravityLocal = game_mech.Gravity_Global
        on_surface = 0
        for wall_group in fn_UI.wall_types_for_beat_calc:
            for wall_type in wall_group:
                for wall in getattr(self.GameMap, wall_type):
                    (ball_point, on_surface) = self.WallBeatCalculate(wall, dt, ball_point, ball_radius, on_surface)
        self.CBall.MoveBall(ball_point)
        self.CBall.Spin(dt)
        self.MoveScreen(dt)
        self.CBall.velocity = game_mech.AddVector(self.CBall.velocity, GravityLocal, 1, dt) 
        self.CBall.on_surface = on_surface     
                
    # управление отрисовкой
    def to_game_coords(self, widget, pos):
        window_pos = widget.to_window(pos[0], pos[1], False)
        game_pos = self.to_widget(window_pos[0], window_pos[1], False)
        return game_pos
               
    def CheckWindowX(self, new_x, padding, game_mod):
        # game_mod: 1 - don't run, 0 - run
        scale = self.scale        
        if self.small_game_map[2*game_mod] == 1:
            return - (self.GameMap.min_x * scale)
        if - new_x < (self.GameMap.min_x * scale):
            return - (self.GameMap.min_x * scale)
        if - new_x > (self.GameMap.max_x * scale - self.game_window_size[0] + padding):
            logger.InsertLog((new_x, self.GameMap.max_x, scale, self.game_window_size[0], padding ))
            return - (self.GameMap.max_x * scale - self.game_window_size[0] + padding)    
        return new_x  
            
    def CheckWindowY(self, new_y, padding, game_mod):
        # game_mod: 1 - don't run, 0 - run
        scale = self.scale
        if self.small_game_map[1 + 2*game_mod] == 1:
            return - (self.GameMap.max_y * scale - self.game_window_size[1])  
        if - new_y > (self.GameMap.max_y * scale - self.game_window_size[1]):
            return - (self.GameMap.max_y * scale - self.game_window_size[1])  
        if - new_y < (self.GameMap.min_y * scale - padding):
            return - (self.GameMap.min_y * scale - padding)
        return new_y
    
    def MoveScreen(self, dt):
        Ball = self.CBall.center
        BallVel = self.CBall.velocity
        scale = self.scale
        if self.small_game_map[0] == 0:
            if BallVel[0] < 0 and (self.GameMap.max_x - Ball[0]) * scale > self.game_window_size[0] * 0.3 and self.game_window_x < - (self.GameMap.min_x*scale): 
                self.game_window_x -= BallVel[0]*dt
            if BallVel[0] > 0 and (Ball[0] - self.GameMap.min_x) * scale > self.game_window_size[0] * 0.3 and self.game_window_x > - (self.GameMap.max_x*scale - self.game_window_size[0]): 
                self.game_window_x -= BallVel[0]*dt
            self.game_window_x = self.CheckWindowX(self.game_window_x, 0, 0)
                  
        if self.small_game_map[1] == 0:
            if BallVel[1] < 0 and (self.GameMap.max_y - Ball[1]) * scale > self.game_window_size[1] * 0.3 and self.game_window_y < - (self.GameMap.min_y*scale): 
                self.game_window_y -= BallVel[1]*dt
            if BallVel[1] > 0 and (Ball[1] - self.GameMap.min_y) * scale > self.game_window_size[1] * 0.3 and self.game_window_y > - (self.GameMap.max_y*scale - self.game_window_size[1]): 
                self.game_window_y -= BallVel[1]*dt
            self.game_window_y = self.CheckWindowY(self.game_window_y, 0, 0)
        
        if self.small_game_map[0] == 0 or self.small_game_map[1] == 0:
            self.pos = self.game_window
        
    def SetStartGameWindow(self):
        # set window_x
        scale = self.scale
        logger.InsertLog(self.small_game_map)
        if self.small_game_map[0] == 1:
            self.game_window_x = - self.GameMap.min_x * scale
        else:
            self.game_window_x = - (self.CBall.center_x * scale - self.game_window_size[0] * 0.5)
            if self.game_window_x > - (self.GameMap.min_x * scale):
                self.game_window_x =  (self.GameMap.min_x * scale)
            if self.game_window_x < - (self.GameMap.max_x * scale - self.game_window_size[0]):
                  self.game_window_x = - (self.GameMap.max_x * scale - self.game_window_size[0])                     # set window_y         
        if self.small_game_map[1] == 1:
            self.game_window_y = - (self.GameMap.max_y * scale - self.game_window_size[1])
        else:
            self.game_window_y = - (self.CBall.center_y * scale - self.game_window_size[1] * 0.7)
            if self.game_window_y > - (self.GameMap.min_y * scale):
                self.game_window_y =  (self.GameMap.min_y * scale)
            if self.game_window_y < - (self.GameMap.max_y * scale - self.game_window_size[1]):
                  self.game_window_y = - (self.GameMap.max_y * scale - self.game_window_size[1])   
        self.pos = self.game_window       
           
    def ReadGameWindowSize(self):
        EventLoop.ensure_window()
        self.game_window_size = (EventLoop.window.size[0], EventLoop.window.size[1] - fn_UI.TopLabelSize())  
        
    def SetGameScaling(self, value):
        self.do_translation = value
        self.do_scale = value
        
    def ResizeGame(self, size = None):
        if size is None:
            self.ReadGameWindowSize()
        else:
            self.game_window_size = size
        if self.game_window_size[0] <= self.game_window_size[1]:
            self.vertical_window = True
        else:
            self.vertical_window = False
        self.game_menu_width = fn_UI.GameMenuWidth()
        self.ReadGameMapSize()
        self.CheckIsMapSmall()
        self.SetStartGameWindow()        
        
    # Методы взаимодействия с картой   
    
    def CreateBall(self):
        if self.CBall is None:
            CBall = ball_mech.Ball()
            CBall.id = 'CBallId'
            CBall.WriteInCenter(0)
            self.CBall = CBall
        self.add_widget(self.CBall)
        if not self.GameMap is None:
            self.CBall.center =self.GameMap.CBall
        self.CBall.velocity = (0, 0)
        self.CBall.angle_velocity = 0.0
        self.CBall.angle = 0
        
    def ReadGameMapSize(self):
        self.game_map_width, self.game_map_height = self.GameMap.game_map_size 
        self.game_map_pos = (self.GameMap.min_x, self.GameMap.min_y)  
        self.scale_min = min(self.game_window_size[0]/self.game_map_width, self.game_window_size[1]/self.game_map_height)
        
    def CreateWalls(self):
        if not self.GameMap is None:
            for wall in self.GameMap.Walls + self.GameMap.RWalls + self.GameMap.SSWalls + self.GameMap.SRWalls + self.GameMap.JSWalls:
                self.add_widget(wall)
                                        
    def CheckIsMapSmall(self):
        scale = self.scale
        menu_size = self.game_menu_width
        if self.game_map_width * scale <= self.game_window_size[0]:
            self.small_game_map[0] = 1
        else:
            self.small_game_map[0] = 0
        if self.game_map_height * scale <= self.game_window_size[1]:
            self.small_game_map[1] = 1
        else:
            self.small_game_map[1] = 0
        if self.game_map_width * scale <= self.game_window_size[0] - menu_size:
            self.small_game_map[2] = 1
        else:
            self.small_game_map[2] = 0
        if self.game_map_height  * scale <= self.game_window_size[1] - menu_size:
            self.small_game_map[3] = 1
        else:
            self.small_game_map[3] = 0        
    
    # методы управления игрой    
        
    def RunGame(self):
        self.life_time = 0
        self.SetGameScaling(False)
        self.SetStartGameWindow()
        self.game_schedule = Clock.schedule_interval(self.MoveGame, 1.0/game_mech.FPS)
        
    def StopGame(self):
        self.life_time = 0
        self.scale = 1.0
        self.SetGameScaling(True)
        self.remove_widget(self.CBall)
        self.CreateBall()  
        self.CheckIsMapSmall()
        self.SetStartGameWindow()
        
    def PauseGame(self):
        self.SetGameScaling(True)
        
    def ResumeGame(self):
        self.SetGameScaling(False)
        self.game_schedule = Clock.schedule_interval(self.MoveGame, 1.0/game_mech.FPS)
        
    def LoadGame(self):
        self.clear_widgets()
        self.ReadGameWindowSize()
        self.game_menu_width = fn_UI.GameMenuWidth()
        self.GameMap = GM.GameMap()
        self.GameMap.LoadInitialMap('level0')
        self.GameMap.ProcessMap()
        self.ReadGameMapSize()
        self.CheckIsMapSmall()
        self.CreateBall()
        self.CreateWalls()
        self.SetGameScaling(True)
        self.SetStartGameWindow()
#        self.RunGame()
        
    def CloseGame(self):
        self.SetGameScaling(False)
        self.GameMap.ClearLevel()

