import fn_UI

class LevelListScr(fn_UI.CBall_Screen):
    pass
   
def AddNecessaryLists(function):
    def wrapper():
        map = function()
        for WType in fn_UI.wall_types+fn_UI.instruments_types:
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
    ],
    'InstrSmooth': [
            (1, 200, 'M'),
            (2, 100, 'S')
    ]
    
    }
    return LevelMap
    
    
    
GiveLevel = {
'level0': level0,

}
 