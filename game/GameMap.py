import io
import game.drawing
import game.StraitWall as SW
import game.RoundWall as RW
import game.Smoothy as SmW
import game.Jumpy as JW
import game.AngleWall as AW
import game.Ball as ball_mech
import game.mechanics as game_mech
import logger
import levellist.levellist as llist
import fn_UI
import constants

class GameMap():
    min_x = None
    min_y = None
    max_x = None
    max_y = None
    game_map_size = (0,0)
    Walls = []
    RWalls = []
    AWalls = []
    SSWalls = []
    SRWalls = []
    JSWalls = []
    initial_map = None
    
    def LoadInitialMap(self, LevelName):
        self.initial_map = llist.GiveLevel[LevelName]()
        self.ReadLevel()
    
    def ReadLevel(self):
        map = self.initial_map
        self.CBall = map['CBall']
        for wall in map['Walls']:
            self.Walls.append(SW.StraitWall(input_data_line = wall))
        for wall in map['RWalls']:
            self.Walls.append(RW.RoundWall(input_data_line = wall))
        for wall in map['SSWalls']:
            self.Walls.append(SmW.SmoothyStraitWall(input_data_line = wall))
        for wall in map['SRWalls']:
            self.Walls.append(SmW.SmoothyRoundWall(input_data_line = wall))
        for wall in map['JSWalls']:
            self.Walls.append(JW.JumpyStraitWall(input_data_line = wall))
        
    def AddAngleWall(self, EndWall, StartWall):
        Angle = EndWall.End
        StartNormal = EndWall.NormalVec(Angle)
        EndNormal = StartWall.NormalVec(Angle)
        if game_mech.VectorMult((0,0), StartNormal, EndNormal) < 0:
            logger.InsertLog("Angle found: "+str(Angle))
            self.AWalls.append(AW.Angle(Angle, StartNormal=StartNormal, EndNormal=EndNormal))
    
    def WallStartEndCheck(self, Wall, wallnumber):
        walltype = type(Wall).__name__
        start_found = 0
        end_found = 0
        for wtype in constants.wall_types:
            for lwall in getattr(self, wtype):                
                if Wall.Start_x == lwall.End_x and  Wall.Start_y == lwall.End_y:
                    start_found = 1    
                if Wall.End_x == lwall.Start_x and  Wall.End_y == lwall.Start_y:
                    end_found = 1  
                    self.AddAngleWall(Wall, lwall)
        if start_found == 0:
            logger.InsertLog('У стены '+ walltype +' ' +str(wallnumber)+' начало ни с чем не соединено: '+str(Wall.Start))
        if end_found == 0:
            logger.InsertLog('У стены '+ walltype +' ' +str(wallnumber)+' конец ни с чем не соединен: '+str(Wall.End))
            
    def UpdateMapBoundaries(self, wall):
        if self.max_x is None:
            self.max_x = wall.End_x
            self.min_x = wall.End_x
            self.max_y = wall.End_y
            self.min_y = wall.End_y
        if wall.End_x > self.max_x:
            self.max_x = wall.End_x
        if wall.End_x < self.min_x:
            self.min_x = wall.End_x
        if wall.End_y > self.max_y:
            self.max_y = wall.End_y
        if wall.End_y < self.min_y:
            self.min_y = wall.End_y
   
    def CheckWallsInList(self, Walls):
         for wallnumber, wall in enumerate(Walls):
            self.WallStartEndCheck(wall, wallnumber)
            self.UpdateMapBoundaries(wall)
                                                    
    def ProcessMap(self):
        for wtype in constants.wall_types:
            self.CheckWallsInList(getattr(self, wtype))
        logger.InsertLog("Map size " + str((self.max_x, self.max_y)))
        self.game_map_size = (self.max_x - self.min_x, self.max_y - self.min_y)
        
