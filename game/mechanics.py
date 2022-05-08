from kivy.vector import Vector
from typing import Tuple, Optional
#import numpy as np

Point = Tuple[float, float]


FPS = 100
Ball_radius = 120
Gravity_Global = (0, -800)
Gravity_Global_abs = (Gravity_Global[0]**2+Gravity_Global[1]**2)**0.5
angle_velocity_convertation_max_value = 200
angle_velocity_convertation_coeff = 0.63 # коэффициент между кинетическими энероиями поступательного и вращательного движений шара

def AddVector(vec1, vec2, dt1=1, dt2=1):
    return (round(vec1[0]*dt1+vec2[0]*dt2, 2), round(vec1[1]*dt1+vec2[1]*dt2, 2))
    
def LineLength(x, y):
    return (x**2+y**2)**0.5
    
def VectorMult(p0: Point, p1: Point, p2: Point):
    # p0 - общая вершина, p1 - вторая вершина основания, p2 - конец второго вектора
    ret = (p2[0]-p1[0])*(p0[1] - p1[1])-(p0[0]-p1[0])*(p2[1]-p1[1])
    return ret