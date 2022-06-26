


LevelGridColsCount = 5

wall_types = ('Walls', # простые прямые стены
        'RWalls',  # простые круглые стены
#        'AWalls',  # углы между стенами, в которые может ударить шар
        'SSWalls',  # мягкие прямые стены
        'SRWalls',  # мягкие круглые стены
        'JSWalls',  # упругие прямые стены
)

wall_types_for_beat_calc = (
        ('JSWalls',
        'SSWalls',
        'SRWalls'
        ) ,
        ('Walls',
        'RWalls',
        'AWalls'
        )
)

interface_background_color = (0.2, 0.35, 0.5, 1)
button_pict_color = (0.8, 0.8, 0.8, 1)