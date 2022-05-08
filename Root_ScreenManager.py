# Создаем менеджер экранов и прописываем в нем функции для kv
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import mainmenu
import game
import levellist
import settings
import logger

class CBScreenManager_class(ScreenManager):
    BackMapping = {
    'Settings':'MainMenu'
    ,'Game':'LevelList'
    ,'LevelList':'MainMenu'}
    debug = 0
    def __init__(self, **kwargs):
        super(CBScreenManager_class, self).__init__(**kwargs)
        self.add_widget(mainmenu.MainMenuScr(name="MainMenu"))
        self.add_widget(settings.SettingsScr(name="Settings"))
        self.add_widget(levellist.LevelListScr(name="LevelList"))
        self.add_widget(game.GameScr(name="Game"))
        self.current = 'Game'
        Window.bind(on_keyboard=self._key_handler)
        Window.bind(on_resize=self._resize_handler)

    def _key_handler(self, instance, key, *args):
        if key is 27 and self.current != 'MainMenu':
            self.current =self.BackMapping[self.current]
            return True
        else:
            if key is 27 and self.debug == 1:
                raise NameError('Programm ends')
            return False

    def _resize_handler(self, *args):
        if self.current == 'Game':
            self.current_screen.ResizeGame(args[1:])
        return False
