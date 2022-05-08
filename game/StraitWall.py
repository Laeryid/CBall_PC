import game.drawing as drawing
from kivy.properties import NumericProperty
from kivy.properties import  ReferenceListProperty
from kivy.properties import  ListProperty
import game.mechanics as game_mech

class StraitWall(drawing.Wall):
    input_data_line = ListProperty(None)
    Length = NumericProperty(0)
    Normal_x = NumericProperty(0)
    Normal_y = NumericProperty(0)
    Normal = ReferenceListProperty(Normal_x, Normal_y)
    NormalVectStart_x = NumericProperty(0)
    NormalVectStart_y = NumericProperty(0)
    NormalVectEnd_x = NumericProperty(0)
    NormalVectEnd_y = NumericProperty(0)
    Tangent_x = NumericProperty(0)
    Tangent_y = NumericProperty(0)
    Tangent = ReferenceListProperty(Tangent_x, Tangent_y)
    
    
    def __init__(self, *args, **kwargs):
        super(StraitWall, self).__init__(*args, **kwargs)
        if not self.input_data_line is None:
            self.Start_x = int(self.input_data_line[0])
            self.Start_y = int(self.input_data_line[1])
            self.End_x = int(self.input_data_line[2])
            self.End_y = int(self.input_data_line[3])
            self.Length = game_mech.LineLength(self.End_x-self.Start_x, self.End_y-self.Start_y)
            Normal = (self.Start_y-self.End_y, self.End_x-self.Start_x)
            self.Normal_x = Normal[0]/ game_mech.LineLength(Normal[0], Normal[1])
            self.Normal_y = Normal[1]/ game_mech.LineLength(Normal[0], Normal[1])
            self.Tangent_x = (self.End_x-self.Start_x) / self.Length # для единообразия
            self.Tangent_y = (self.End_y-self.Start_y) / self.Length
            self.NormalVectStart_x = (self.Start_x+self.End_x)/2
            self.NormalVectStart_y = (self.Start_y+self.End_y)/2
            self.NormalVectEnd_x = self.NormalVectStart_x + 50.0 * self.Normal_x
            self.NormalVectEnd_y = self.NormalVectStart_y + 50.0 * self.Normal_y
        
    def PointDistance(self, point=(0,0)):
        # Проверяем знак скалярных произведений
        if ((point[0]-self.Start_x)*(self.End_x-self.Start_x)+(point[1]-self.Start_y)*(self.End_y-self.Start_y))>0 and ((point[0]-self.End_x)*(self.Start_x-self.End_x)+(point[1]-self.End_y)*(self.Start_y-self.End_y))> 0:
            # S2 - двойная площадь
            S2 = game_mech.VectorMult(self.Start, self.End, point)
            return abs(S2) / self.Length
        else:
            return None
        
    def NormalVelocity(self, CBall):
        return self.Normal_x*CBall.velocity_x+ self.Normal_y*CBall.velocity_y
        
    def TangentVelocity(self, CBall):
        return self.Tangent_x*CBall.velocity_x+ self.Tangent_y*CBall.velocity_y
        
    def is_appropriate(self, dt, CBall):
        normal_vel_abs= self.NormalVelocity(CBall)
        return normal_vel_abs <= 0.0 or abs(normal_vel_abs*dt) <= 1.0
        
    def NormalVec(self, point):
        return self.Normal
        
    def TangentVec(self, point):
        return self.Tangent
        
        