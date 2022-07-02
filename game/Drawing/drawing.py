from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
import logger

class Wall(Widget):
    Start_x = NumericProperty(None)
    Start_y = NumericProperty(None)
    Start = ReferenceListProperty(Start_x, Start_y)
    End_x = NumericProperty(None)
    End_y = NumericProperty(None)
    End = ReferenceListProperty(End_x, End_y)
    # часть танг скорости, которую теряет при ударе
    tangent_vel_loosing = NumericProperty(0)
    # трение при качении по поверхности
    friction_coeff = NumericProperty(0)
    friction_abs = NumericProperty(10)
    is_activ = NumericProperty(0)
    resilience = NumericProperty(2)
    resiliencecoeff = NumericProperty(None)
    is_safe = NumericProperty(0)
    color = ListProperty((0.8, 0.8, 0.8, 1.0))
    
    resilience_dict = {
    0: 0.2  # неупругий
    , 1: 0.5 # нормальный
    , 2: 1.0 # упругий
    }
        
    def __init__(self, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.resiliencecoeff = self.resilience_dict[self.resilience]
        
    def PointDistance(self, point=(0,0)):
        logger.InsertLog('Method is not created')
    
    def NormalVelocity(self, CBall):
        logger.InsertLog('Method is not created')                
    def TangentVelocity(self, CBall):
        logger.InsertLog('Method is not created')
        
    def is_appropriate(self, dt, CBall):
        logger.InsertLog('Method is not created')
        
    def NormalVec(self, point):
        logger.InsertLog('Method is not created')
        
    def TangentVec(self, point):
        logger.InsertLog('Method is not created')
        
    