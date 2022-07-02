import game.Drawing.StraitWall as SW
import game.Drawing.RoundWall as RW
from kivy.properties import NumericProperty, ListProperty

smooth_friction = 0.1
smooth_tangent_loosing = 0.5
smooth_color = (0.6, 1, 0.6, 1.0)

class SmoothyStraitWall(SW.StraitWall):
    is_safe = NumericProperty(1)
    resilience = NumericProperty(0)
    friction_coeff = NumericProperty(smooth_friction) 
    tangent_vel_loosing = NumericProperty(smooth_tangent_loosing)
    color = ListProperty(smooth_color)
    
    
class SmoothyRoundWall(RW.RoundWall):
    is_safe = NumericProperty(1)
    resilience = NumericProperty(0)
    friction_coeff = NumericProperty(smooth_friction) 
    color = ListProperty(smooth_color)