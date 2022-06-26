import fn_UI
import game.Ball as ball_mech
import game.mechanics as game_mech
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, ReferenceListProperty, BooleanProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.base import EventLoop
from kivy.vector import Vector
import game.GameMap as GM
import logger
import game.AngleWall as AW
import game.GameMenu as game_menu
from math import floor

class Game(RelativeLayout):
    CBall  = ObjectProperty(None)
    GameMap = ObjectProperty(None)
    life_time = NumericProperty(None)
    game_window_x = NumericProperty(0)
    game_window_y = NumericProperty(0)
    game_window = ReferenceListProperty(game_window_x, game_window_y)
    scale = NumericProperty(1)
    game_window_size = ListProperty((0,0))
    vertical_window = BooleanProperty(True)
    game_map_width = NumericProperty(0)
    game_map_height = NumericProperty(0)
    game_map_size = ReferenceListProperty(game_map_width, game_map_height)
    game_map_pos = ListProperty((0,0))
    small_game_map = ListProperty((0,0,0,0)) # карта маленькая в обычном режиме, карта маленькая в режиме перетаскивания
    avcmv = game_mech.angle_velocity_convertation_max_value
    status = NumericProperty(0)
    touch_x = NumericProperty(None)
    touch_y = NumericProperty(None)
    game_window_x_on_touch = NumericProperty(0)
    game_window_y_on_touch = NumericProperty(0)
    last_second_frames = NumericProperty(0)
    top_label_size = NumericProperty(fn_UI.TopLabelSize())
    
    game_status_dict = {
            0: "Loaded"     ,
            1: "Executing" ,
            2: "Pause"
            }
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_x, self.touch_y = touch.pos
            self.game_window_x_on_touch, self.game_window_y_on_touch = self.game_window
        return super(Game, self).on_touch_down(touch)
        
    def on_touch_move(self, touch):
        if self.status == 0 and  self.collide_point(*touch.pos):
            if self.small_game_map[2] == 0:
                if self.touch_x is None:
                    self.touch_x = touch.x
                if self.game_window_x_on_touch is None:
                    self.game_window_x_on_touch = self.game_window_x
                new_window_x = self.game_window_x_on_touch - self.touch_x + touch.x                
                self.game_window_x = self.CheckWindowX(new_window_x)
            if self.small_game_map[3] == 0:
                if self.touch_y is None:
                    self.touch_y = touch.y
                if self.game_window_y_on_touch is None:
                    self.game_window_y_on_touch = self.game_window_y
                new_window_y = self.game_window_y_on_touch - self.touch_y + touch.y            
                self.game_window_y = self.CheckWindowY(new_window_y)
            return True
        return super(Game, self).on_touch_move(touch)
    
    def CalcFPS(self, dt):
        seconds_check = self.life_time - floor(self.life_time)
        if seconds_check + dt > 1.0:
            # секунда накопилась            
            self.CBall.WriteInCenter(self.last_second_frames)
            self.last_second_frames = 0
        self.last_second_frames += 1
    
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
        
    def CreateWalls(self):
        if not self.GameMap is None:
            for wall in self.GameMap.Walls + self.GameMap.RWalls + self.GameMap.SSWalls + self.GameMap.SRWalls + self.GameMap.JSWalls:
                self.add_widget(wall)
            
                            
    def CheckIsMapSmall(self):
        menu_size = fn_UI.GameMenuWidth()
        if (self.GameMap.max_x-self.GameMap.min_x) * self.scale <= self.game_window_size[0]:
            self.small_game_map[0] = 1
        else:
            self.small_game_map[0] = 0
        if (self.GameMap.max_y-self.GameMap.min_y) * self.scale <= self.game_window_size[1]:
            self.small_game_map[1] = 1
        else:
            self.small_game_map[1] = 0
        if (self.GameMap.max_x-self.GameMap.min_x) * self.scale <= self.game_window_size[0] - menu_size:
            self.small_game_map[2] = 1
        else:
            self.small_game_map[2] = 0
        if (self.GameMap.max_y-self.GameMap.min_y) * self.scale <= self.game_window_size[1] - menu_size:
            self.small_game_map[3] = 1
        else:
            self.small_game_map[3] = 0            

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
                
    def CheckWindowX(self, new_x):
        right_padding = 0
        if self.status == 0 and not self.vertical_window:
            right_padding = fn_UI.GameMenuWidth()
            if self.small_game_map[2] == 1:
                return - ((self.GameMap.max_x + self.GameMap.min_x) * self.scale - self.game_window_size[
                    0] + right_padding) * 0.5
        if self.small_game_map[0] == 1:
            return - ((self.GameMap.max_x + self.GameMap.min_x) * self.scale - self.game_window_size[0]) * 0.5
        if - new_x < (self.GameMap.min_x * self.scale):
            return - (self.GameMap.min_x * self.scale)
        if - new_x > (self.GameMap.max_x * self.scale - self.game_window_size[0] + right_padding):
            return - (self.GameMap.max_x * self.scale - self.game_window_size[0] + right_padding)

        return new_x  
            
    def CheckWindowY(self, new_y):
        bot_padding = 0
        if self.status == 0 and self.vertical_window:
            bot_padding = fn_UI.GameMenuWidth()
            if self.small_game_map[3] == 1:
                return - ((self.GameMap.max_y + self.GameMap.min_y) * self.scale - self.game_window_size[1]) * 0.5
        if self.small_game_map[1] == 1:
            return - ((self.GameMap.max_y + self.GameMap.min_y) * self.scale - self.game_window_size[1]) * 0.5
        if - new_y < (self.GameMap.min_y * self.scale - bot_padding):
            return - (self.GameMap.min_y * self.scale - bot_padding)
        if - new_y > (self.GameMap.max_y * self.scale - self.game_window_size[1] + self.top_label_size):
            return - (self.GameMap.max_y * self.scale - self.game_window_size[1] + self.top_label_size)

        return new_y
    
    def MoveScreen(self, dt):
        Ball = self.CBall.center
        BallVel = self.CBall.velocity
        if self.small_game_map[0] == 0:
            if BallVel[0] < 0 and (self.GameMap.max_x - Ball[0]) * self.scale > self.game_window_size[0] * 0.3 and self.game_window_x < - (self.GameMap.min_x*self.scale): 
                self.game_window_x -= BallVel[0]*dt
            if BallVel[0] > 0 and (Ball[0] - self.GameMap.min_x) * self.scale > self.game_window_size[0] * 0.3 and self.game_window_x > - (self.GameMap.max_x*self.scale - self.game_window_size[0]): 
                self.game_window_x -= BallVel[0]*dt
            self.game_window_x = self.CheckWindowX(self.game_window_x)
                  
        if self.small_game_map[1] == 0:
            if BallVel[1] < 0 and (self.GameMap.max_y - Ball[1]) * self.scale > self.game_window_size[1] * 0.3 and self.game_window_y < - (self.GameMap.min_y*self.scale): 
                self.game_window_y -= BallVel[1]*dt
            if BallVel[1] > 0 and (Ball[1] - self.GameMap.min_y) * self.scale > self.game_window_size[1] * 0.3 and self.game_window_y > - (self.GameMap.max_y*self.scale - self.game_window_size[1]): 
                self.game_window_y -= BallVel[1]*dt
            self.game_window_y = self.CheckWindowY(self.game_window_y)

    def SetScale(self):
        if self.vertical_window == True:
            self.scale  =  self.game_window_size[0] * 0.1 / game_mech.Ball_radius
        else:
            self.scale  =  self.game_window_size[1] * 0.1 / game_mech.Ball_radius
        if self.scale > 1.0:
            self.scale = 1

    def SetGameWindow(self):
        self.SetScale()
        # set window_x
        if self.small_game_map[0] == 1:
            self.game_window_x = - (
                        (self.GameMap.max_x + self.GameMap.min_x) * self.scale - self.game_window_size[0]) * 0.5
        else:
            self.game_window_x = - (self.CBall.center_x * self.scale - self.game_window_size[0] * 0.5)
            if - self.game_window_x < (self.GameMap.min_x * self.scale):
                self.game_window_x = - (self.GameMap.min_x * self.scale)
            if - self.game_window_x > (self.GameMap.max_x * self.scale - self.game_window_size[0]):
                  self.game_window_x = - (self.GameMap.max_x * self.scale - self.game_window_size[0])
        # set window_y
        if self.small_game_map[1] == 1:
            self.game_window_y = - (
                        (self.GameMap.max_y + self.GameMap.min_y) * self.scale - self.game_window_size[1]) * 0.5
        else:
            self.game_window_y = - (self.CBall.center_y * self.scale - self.game_window_size[1] * 0.7)
            if - self.game_window_y < (self.GameMap.min_y * self.scale):
                self.game_window_y = - (self.GameMap.min_y * self.scale)
            if - self.game_window_y > (self.GameMap.max_y * self.scale - self.game_window_size[1]):
                  self.game_window_y = - (self.GameMap.max_y * self.scale - self.game_window_size[1])

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
#        self.CBall.WriteInCenter(self.CBall.on_surface)

        for wall_group in fn_UI.wall_types_for_beat_calc:
            for wall_type in wall_group:
                for wall in getattr(self.GameMap, wall_type):
                    (ball_point, on_surface) = self.WallBeatCalculate(wall, dt, ball_point, ball_radius, on_surface)
        self.CBall.MoveBall(ball_point)
        self.CBall.Spin(dt)
        self.MoveScreen(dt)
        self.CBall.velocity = game_mech.AddVector(self.CBall.velocity, GravityLocal, 1, dt) 
        self.CBall.on_surface = on_surface
   
    def ReadGameWindowSize(self):
        EventLoop.ensure_window()
        self.game_window_size = (EventLoop.window.size[0], EventLoop.window.size[1] - fn_UI.TopLabelSize())

    def ReadGameMapSize(self):
        self.game_map_width, self.game_map_height = self.GameMap.game_map_size 
        self.game_map_pos = (self.GameMap.min_x, self.GameMap.min_y)

    def SetVertical(self):
        if self.game_window_size[0] <= self.game_window_size[1]:
            self.vertical_window = True
        else:
            self.vertical_window = False

    def ResizeGame(self, size = None):
        if size is None:
            self.ReadGameWindowSize()
        else:
            self.game_window_size = size
        self.SetVertical()
        self.CheckIsMapSmall()
        self.SetGameWindow()
        logger.InsertLog(self.game_window_size)
        
    def RunGame(self):
        self.life_time = 0
        self.SetGameWindow()
        self.game_schedule = Clock.schedule_interval(self.MoveGame, 1.0/game_mech.FPS)
        
    def StopGame(self):
#        if self.game_schedule:
#            self.game_schedule.cancel()  
        self.life_time = 0
        self.remove_widget(self.CBall)
        self.CreateBall()  
        self.SetGameWindow()
        
    def PauseGame(self):
#        self.game_schedule.cancel()  
        pass
        
    def ResumeGame(self):
        self.game_schedule = Clock.schedule_interval(self.MoveGame, 1.0/game_mech.FPS)
        
    def LoadGame(self):
        self.clear_widgets()
        self.GameMap = GM.GameMap()
        self.GameMap.LoadInitialMap('level0')
        self.GameMap.ProcessMap()
        self.ReadGameMapSize()
        self.CreateBall()
        self.CreateWalls()
        self.ReadGameWindowSize()
        self.SetVertical()
        self.CheckIsMapSmall()
        self.SetGameWindow()
        logger.InsertLog(self.game_window_size)
#        self.RunGame()