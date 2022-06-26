import constants
import CBall_Screen

class LevelListScr(CBall_Screen.CBall_Screen):
    pass
   
def AddNecessaryLists(function):
    def wrapper():
        map = function()
        for WType in constants.wall_types:
                    if not WType in map:
                        map[WType] = []
        return map
        
    return wrapper

@AddNecessaryLists
def level0():
    LevelMap = {
    'CBall': (800, 1700), 
    'Walls': [
            (-300,0,300,0),
            (1500,600, 1500,1900),
            (1500,1900,-300,1900),
            (-300, 1900, -300, 0) 
    ],
    'RWalls': [
            (300, 300, 300, 90, 180)
    ],
    'JSWalls': [
            (600, 300, 1500, 600)
    ]
    
    }
    return LevelMap
    
    
    
GiveLevel = {
'level0': level0,

}
 