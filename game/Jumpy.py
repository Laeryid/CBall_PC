import game.StraitWall as SW
from kivy.properties import NumericProperty, ListProperty

jumpy_color = (0.7, 0.7, 1.0, 1.0)

class JumpyStraitWall(SW.StraitWall):
    is_safe = NumericProperty(1)
    resilience = NumericProperty(2)
    color = ListProperty(jumpy_color)
    