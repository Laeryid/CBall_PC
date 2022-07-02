import game.Drawing.drawing as drawing
import game.mechanics as game_mech
from typing import Tuple

class Angle(drawing.Wall):
    StartNormal: Tuple 
    EndNormal: Tuple
    StartNormalPoint: Tuple
    EndNormalPoint: Tuple
    
    def __init__(self, *args, **kwargs):
        super(Angle, self).__init__()
        if len(args)>0:
            self.Start = args[0]
        else:
            self.Start = (0,0)
        self.End = self.Start
        self.StartNormal = kwargs["StartNormal"]
        self.EndNormal = kwargs["EndNormal"]
        self.StartNormalPoint = (self.Start_x + self.StartNormal[0], self.Start_y + self.StartNormal[1])
        self.EndNormalPoint = (self.End_x + self.EndNormal[0], self.End_y + self.EndNormal[1])
    
    def PointDistanceFast(self, point=(0,0)):
        return game_mech.LineLength(self.Start_x-point[0],self.Start_y-point[1])
    
    def PointDistance(self, point=(0,0)):
        # проверяем, что концы нормалей с разных сторон
        if game_mech.VectorMult(self.Start, point, self.StartNormalPoint)*game_mech.VectorMult(self.Start, point, self.EndNormalPoint) <= 0:
            return self.PointDistanceFast(point)
        return None
    
    def NormalVelocity(self, CBall):
        Normal = self.NormalVec(CBall.center)
        return Normal[0]*CBall.velocity_x+ Normal[1]*CBall.velocity_y
            
    def TangentVelocity(self, CBall):
        Tangent = self.TangentVec(CBall.center)
        return Tangent[0]*CBall.velocity_x+ Tangent[1]*CBall.velocity_y
        
    def is_appropriate(self, dt, CBall):
        distance = self.PointDistanceFast(CBall.center)
        if abs(distance) <= CBall.radius + dt*game_mech.LineLength(CBall.velocity_x, CBall.velocity_y):
            return True
        return False
        
    def NormalVec(self, point):
        v_x = point[0] - self.Start_x
        v_y = point[1] - self.Start_y
        ln = game_mech.LineLength(v_x, v_y)
        return (v_x/ln, v_y/ln)
        
    def TangentVec(self, point):
        Normal = self.NormalVec(point)
        return (Normal[1],-Normal[0])
    