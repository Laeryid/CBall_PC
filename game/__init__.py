from kivy.lang import Builder
# from game.game import GameScr
from game.GameScr import GameScr
import game.Ball
import game.GameMenu
import game.Drawing.drawing

Builder.load_file('game/Game.kv')
Builder.load_file('game/GameScr.kv')
Builder.load_file('game/Ball.kv')
Builder.load_file('game/GameMenu.kv')

