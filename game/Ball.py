from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Ellipse, Color
from kivy.properties import NumericProperty, ReferenceListProperty, OptionProperty, StringProperty
import game.mechanics as game_mech
import logger.logger as logger
from math import pi

class Ball(RelativeLayout):
    radius = NumericProperty(game_mech.Ball_radius)
    toughnes = NumericProperty(0)
    resilience = NumericProperty(1)
    resiliencecoeff = NumericProperty(None)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    angle = NumericProperty(0)
    angle_velocity = NumericProperty(0)
    on_surface = NumericProperty(0)
    text_on_Ball = StringProperty('')
    toughness_dict = {
    0: "Хрупкий"
    , 1: "Прочный"
    }
    resilience_dict = {
    0: 0.1  # неупругий
    , 1: 0.5 # нормальный
    , 2: 0.9 # упругий
    }
    def __init__(self, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)
        self.size_hint = (None, None)  
        self.resiliencecoeff = self.resilience_dict[self.resilience]
        
        
    def NextPos(self, dt):
        return  game_mech.AddVector(self.center, self.velocity, 1, dt)
    
    def MoveBall(self, center):
        self.center = center
    
    def WriteInCenter(self, text):
        self.text_on_Ball = str(text)
     
    def Spin(self, dt):
        angle = self.angle + self.angle_velocity * dt / self.radius * 180 / pi
        if angle > 360:
            angle -= 360
        if angle < 0:
            angle += 360
        self.angle = angle