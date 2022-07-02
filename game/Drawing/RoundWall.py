import game.Drawing.drawing as drawing
from kivy.properties import NumericProperty
from kivy.properties import  ListProperty
import game.mechanics as game_mech
from math import sin, cos, pi

class RoundWall(drawing.Wall):
    input_data_line = ListProperty(None)
    radius = NumericProperty(0)
    inner_surface = NumericProperty(1)
    angle_start = NumericProperty(0)
    angle_end = NumericProperty(360)
    Center = ListProperty(None)
    angle_mid = ListProperty(None)
    
    def __init__(self, *args, **kwargs):
        super(RoundWall, self).__init__(*args, **kwargs)
        if not self.input_data_line is None:
            self.radius = int(self.input_data_line[2])
            self.center_x = int(self.input_data_line[0])
            self.center_y = int(self.input_data_line[1])
            self.angle_start = int(self.input_data_line[3])
            self.angle_end = int(self.input_data_line[4])
            if len(self.input_data_line)>6:
                self.inner_surface = int(self.input_data_line[5])
            self.Center = (self.x+self.radius, self.y+self.radius)
            if self.inner_surface == 1:
                self.End_x = round(self.Center[0] + self.radius * sin(self.angle_start /180*pi), 2)
                self.End_y = round(self.Center[1] + self.radius * cos(self.angle_start /180*pi), 2)
                self.Start_x = round(self.Center[0] + self.radius * sin(self.angle_end /180*pi), 2)
                self.Start_y = round(self.Center[1] + self.radius * cos(self.angle_end/180*pi), 2)             
            else:                
                self.Start_x = round(self.Center[0] + self.radius * sin(self.angle_start /180*pi), 2)
                self.Start_y = round(self.Center[1] + self.radius * cos(self.angle_start /180*pi), 2)
                self.End_x = round(self.Center[0] + self.radius * sin(self.angle_end /180*pi), 2)
                self.End_y = round(self.Center[1] + self.radius * cos(self.angle_end/180*pi), 2)
            self.angle_mid = (self.Center[0] + self.radius*sin((self.angle_end-self.angle_start) /180*pi), self.Center[1] + self.radius*cos((self.angle_end-self.angle_start) /180*pi))
                    
    def NormalVec(self, point):
        Normal_x = self.x+self.radius - point[0]
        Normal_y = self.y+self.radius - point[1]
        len = game_mech.LineLength(Normal_x, Normal_y) *(2*self.inner_surface-1)
        return (Normal_x/len, Normal_y/len)
        
    def TangentVec(self, point):
        Normal = self.NormalVec(point)
        return (Normal[1],-Normal[0])
        
    def PointDistanceToCenter(self, point):
        return game_mech.LineLength(self.x+self.radius - point[0], self.y + self.radius - point[1])
        
    def PointDistance(self, point):
        # проверяем, что концы дуги с разных сторон, а направление на точку такое же, как и на середину дуги
        if game_mech.VectorMult(self.Center, point, self.Start)*game_mech.VectorMult(self.Center, point, self.End) <= 0 and ((self.Center[0] - point[0])*(self.Center[0] - self.angle_mid[0]) + (self.Center[1] - point[1])*(self.Center[1] - self.angle_mid[1])) >= 0:
            return (self.radius - self.PointDistanceToCenter(point))*(2*self.inner_surface-1)
        return None
        
    def is_appropriate(self, dt, CBall):
        distance = self.PointDistanceToCenter(CBall.center)
        if abs(distance - self.radius) <= CBall.radius + dt*game_mech.LineLength(CBall.velocity_x, CBall.velocity_y):
            return True
        return False
        
    def NormalVelocity(self, CBall):
        Normal = self.NormalVec(CBall.center)
        return Normal[0]*CBall.velocity_x+ Normal[1]*CBall.velocity_y
            
    def TangentVelocity(self, CBall):
        Tangent = self.TangentVec(CBall.center)
        return Tangent[0]*CBall.velocity_x+ Tangent[1]*CBall.velocity_y
            
        
        