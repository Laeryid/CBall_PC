from kivy.app import App
import Root_ScreenManager as rootsm
import logger

CBScreenManager = rootsm.CBScreenManager_class()

CBScreenManager.debug = 0

logger.ClearLog()

class CBallApp(App):
    def build(self):
        return CBScreenManager

if __name__ == '__main__':
    CBallApp().run()
