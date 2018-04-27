import json
from random import choice

SHIP_CARRIER = 0
SHIP_BATTLESHIP = 1
SHIP_CRUISER = 2
SHIP_SUBMARINE = 3
SHIP_DESTROYER = 4

DIRECTION_NORTH = 1
DIRECTION_WEST = 2
DIRECTION_SOUTH = 3
DIRECTION_EAST = 4

ORIENTATION_HORIZONTAL = 0
ORIENTATION_VERTICAL = 1

FIRE_NOTHING = 0
FIRE_SINGLE = 1
FIRE_DOUBLE_VER = 2
FIRE_DOUBLE_HOR = 3
FIRE_CORNER = 4
FIRE_CROSS_DIA = 5
FIRE_CROSS_PLUS = 6
FIRE_MISSILE = 7
ACTIVATE_SHIELD = 8

PLAYER_SELF = 1
PLAYER_OPPONENT = 2

small_cluster = [
    {"lRow": 0, "hRow": 2, "lCol": 0, "hCol": 2},
    {"lRow": 3, "hRow": 6, "lCol": 0, "hCol": 2},
    {"lRow": 0, "hRow": 2, "lCol": 3, "hCol": 6},
    {"lRow": 3, "hRow": 6, "lCol": 3, "hCol": 6}
]
medium_cluster = [
    {"lRow": 0, "hRow": 4, "lCol": 0, "hCol": 4},
    {"lRow": 5, "hRow": 9, "lCol": 0, "hCol": 4},
    {"lRow": 0, "hRow": 4, "lCol": 5, "hCol": 9},
    {"lRow": 5, "hRow": 9, "lCol": 5, "hCol": 9}
]
large_cluster = [
    {"lRow": 0, "hRow": 4, "lCol": 0, "hCol": 4},
    {"lRow": 5, "hRow": 9, "lCol": 0, "hCol": 4},
    {"lRow": 10, "hRow": 13, "lCol": 0, "hCol": 4},
    {"lRow": 0, "hRow": 4, "lCol": 5, "hCol": 9},
    {"lRow": 5, "hRow": 9, "lCol": 5, "hCol": 9},
    {"lRow": 10, "hRow": 13, "lCol": 5, "hCol": 9},
    {"lRow": 0, "hRow": 4, "lCol": 10, "hCol": 13},
    {"lRow": 5, "hRow": 9, "lCol": 10, "hCol": 13},
    {"lRow": 10, "hRow": 13, "lCol": 10, "hCol": 13}
]


ships_small = ['Battleship 0 6 south',
             'Carrier 1 5 East',
             'Cruiser 4 0 East',
             'Destroyer 2 2 East',
             'Submarine 6 2 north'
             ]

ships_med = ['Battleship 1 0 north',
             'Carrier 3 1 East',
             'Cruiser 9 6 north',
             'Destroyer 7 3 north',
             'Submarine 1 8 East'
             ]
ships_large = ['Battleship 3 13 East',
             'Carrier 1 0 East',
             'Cruiser 4 4 north',
             'Destroyer 2 7 north',
             'Submarine 12 6 north'
             ]

ships_info_small = [
    {'orientation': ORIENTATION_HORIZONTAL, 'low_bound': 1, 'high_bound': 5, 'pivot': 5},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 3, 'high_bound': 6, 'pivot': 0},
    {'orientation': ORIENTATION_HORIZONTAL, 'low_bound': 4, 'high_bound': 6, 'pivot': 0},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 2, 'high_bound': 4, 'pivot': 6},
    {'orientation': ORIENTATION_HORIZONTAL, 'low_bound': 2, 'high_bound': 3, 'pivot': 2}
]
ships_info_med = [
    {'orientation': ORIENTATION_HORIZONTAL, 'low_bound': 3, 'high_bound': 7, 'pivot': 1},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 0, 'high_bound': 3, 'pivot': 1},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 6, 'high_bound': 8, 'pivot': 9},
    {'orientation': ORIENTATION_HORIZONTAL, 'low_bound': 1, 'high_bound': 3, 'pivot': 8},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 3, 'high_bound': 4, 'pivot': 7}
]
ships_info_large = [
    {'orientation': ORIENTATION_HORIZONTAL, 'low_bound': 1, 'high_bound': 5, 'pivot': 0},
    {'orientation': ORIENTATION_HORIZONTAL, 'low_bound': 3, 'high_bound': 6, 'pivot': 13},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 4, 'high_bound': 6, 'pivot': 4},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 6, 'high_bound': 8, 'pivot': 12},
    {'orientation': ORIENTATION_VERTICAL, 'low_bound': 7, 'high_bound': 8, 'pivot': 2}
]


STATE = None
DATA = None
BATTLE_MAP = []
DESTROYED = False
MISSED = True
ENEMY_SHIPS = 0
MAP_SIZE = None

FIRE_COUNT = 0
FIRE_DAMAGED = 0

PREP_CELL = None
MAX_ENERGY_SAVING = 0

PREVIOUS_CELL = None

SHIPS = {
    'Carrier': True,
    'Battleship': True,
    'Cruiser': True,
    'Submarine': True,
    'Destroyer': True
}

SHIPS_CONFIG = None

SHIPS_INFO = [
    {'attacked': False, 'orientation': None, 'low_bound': None, 'high_bound': None, 'health': 5, 'pivot': None},
    {'attacked': False, 'orientation': None, 'low_bound': None, 'high_bound': None, 'health': 4, 'pivot': None},
    {'attacked': False, 'orientation': None, 'low_bound': None, 'high_bound': None, 'health': 3, 'pivot': None},
    {'attacked': False, 'orientation': None, 'low_bound': None, 'high_bound': None, 'health': 3, 'pivot': None},
    {'attacked': False, 'orientation': None, 'low_bound': None, 'high_bound': None, 'health': 2, 'pivot': None},
]

SHIPS_ATTACKED = []

def setState(state):
    global STATE, MAP_SIZE
    STATE = state
    MAP_SIZE = STATE['MapDimension']
    readMap()
    checkPlayerShips()
    checkOpponentShips()

def setAvailCluster(available_cluster):
    global DATA
    DATA['available_cluster'] = available_cluster
def setPrevCell(x, y):
    global PREVIOUS_CELL
    PREVIOUS_CELL = {'X': x, 'Y': y}
def setPastCluster(past_cluster):
    global DATA
    DATA['past_cluster'] = past_cluster
def setFireDirection(direction):
    global DATA
    DATA['fire_direction'] = direction
def setPredictedCell(x, y):
    global DATA
    DATA['predicted_cell'] = x, y
def setHitCell(x, y):
    global DATA
    DATA['hit_cell'] = {'X': x, 'Y': y}
def setEvent(event):
    global DATA
    DATA['previous_event'] = event
def setFireType(fire):
    global DATA
    DATA['fire_type'] = fire
def clearPredictedCell():
    global DATA
    setPrevCell(DATA['predicted_cell'])
    DATA['predicted_cell'] = None
def assignHitCell():
    setHitCell(PREVIOUS_CELL['X'], PREVIOUS_CELL['Y'])
def clearHitCell():
    global DATA
    DATA['hit_cell'] = None
    DATA['reversed'] = False
    clearEventHit()
def clearEventHit():
    global DATA
    DATA['event_hit'] = []
def addEventHit(cell):
    global DATA
    DATA['event_hit'].append(cell['direction'])
    setFireDirection(cell['direction'])
    setPredictedCell(cell['X'], cell['Y'])
def reverseDirection():
    global DATA, PREVIOUS_CELL
    fire_direction = getDirection()
    if fire_direction == DIRECTION_EAST:
        setFireDirection(DIRECTION_WEST)
    elif fire_direction == DIRECTION_WEST:
        setFireDirection(DIRECTION_EAST)
    elif fire_direction == DIRECTION_SOUTH:
        setFireDirection(DIRECTION_NORTH)
    elif fire_direction == DIRECTION_NORTH:
        setFireDirection(DIRECTION_SOUTH)
    PREVIOUS_CELL = DATA['hit_cell']
    DATA['reversed'] = True

def checkAvailability(fire):
    if fire == FIRE_SINGLE:
        return True
    if fire == FIRE_CROSS_PLUS:
        return SHIPS['Cruiser']
    if fire == FIRE_DOUBLE_VER:
        return SHIPS['Destroyer']
    if fire == FIRE_CROSS_DIA:
        return SHIPS['Battleship']
    if fire == FIRE_MISSILE:
        return SHIPS['Submarine']
    if fire == FIRE_CORNER:
        return SHIPS['Carrier']
def checkSpace(fire, x, y):
    direction = DATA['fire_direction']
    cells = []
    if fire == FIRE_SINGLE or fire == FIRE_MISSILE:
        cells.append({'X': x, 'Y': y})
        if fire == FIRE_MISSILE:
            snapshot(x, y)
    if fire == FIRE_CROSS_PLUS:
        cells.append({'X': x, 'Y': y})
        cells.append({'X': x-1, 'Y': y})
        cells.append({'X': x+1, 'Y': y})
        cells.append({'X': x, 'Y': y-1})
        cells.append({'X': x, 'Y': y+1})
    if fire == FIRE_DOUBLE_VER:
        if direction == DIRECTION_WEST or direction == DIRECTION_EAST:
            cells.append({'X': x-1, 'Y': y})
            cells.append({'X': x+1, 'Y': y})
        else:
            cells.append({'X': x, 'Y': y-1})
            cells.append({'X': x, 'Y': y+1})
    if fire == FIRE_CROSS_DIA or fire == FIRE_CORNER:
        if fire == FIRE_CROSS_DIA:
            cells.append({'X': x, 'Y': y})
        cells.append({'X': x-1,'Y': y-1})
        cells.append({'X': x-1, 'Y': y+1})
        cells.append({'X': x+1, 'Y': y-1})
        cells.append({'X': x+1, 'Y': y+1})
    return isValidCell(cells)

def snapshot(x, y):
    global DATA
    snap = []

    for i in range(x-2, x+3):
        row = []
        for j in range(y-2, y+3):
            row.append(BATTLE_MAP[x][y])
        snap.append(row)
    DATA['snap'] = snap


def isValidCell(cells):
    for cell in cells:
        x = cell['X']
        y = cell['Y']
        if x < 0 or x >= MAP_SIZE:
            return False
        if y < 0 or y >= MAP_SIZE:
            return False
        if not isNothing(x, y):
            return False
    return True

def setNextX(fire, direction, prevX):
    if fire == FIRE_SINGLE:
        if direction == DIRECTION_WEST:
            return prevX-1
        elif direction == DIRECTION_EAST:
            return prevX+1
    if fire == FIRE_CROSS_PLUS or fire == FIRE_DOUBLE_VER:
        if direction == DIRECTION_WEST:
            return prevX-2
        elif direction == DIRECTION_EAST:
            return prevX+2
    return prevX
def setNextY(fire, direction, prevY):
    if fire == FIRE_SINGLE:
        if direction == DIRECTION_NORTH:
            return prevY+1
        elif direction == DIRECTION_SOUTH:
            return prevY-1
    if fire == FIRE_CROSS_PLUS or fire == FIRE_DOUBLE_VER:
        if direction == DIRECTION_NORTH:
            return prevY+2
        elif direction == DIRECTION_SOUTH:
            return prevY-1
    return prevY

def getMapSize():
    return MAP_SIZE
def getPrevEvent():
    return DATA['previous_event']
def getPrevCell():
    return PREVIOUS_CELL
def getAvailCluster():
    return DATA['available_cluster']
def getPastCluster():
    return DATA['past_cluster']
def getPrevX():
    cell = getPrevCell()
    return cell['X']
def getPrevY():
    cell = getPrevCell()
    return cell['Y']
def getCluster():
    return DATA['cluster']
def getDirection():
    return DATA['fire_direction']
def getFireType():
    return DATA['fire_type']
def getEnergyReq(ship):
    player = STATE['PlayerMap']['Owner']
    for s in player['Ships']:
        if s['ShipType'] == ship:
            return s['Weapons'][1]['EnergyRequired']
def getPlayerEnergy():
    player = STATE['PlayerMap']['Owner']
    return player['Energy']
def getHitCells():
    return DATA['hit_cells']
def getShieldCharge():
    return STATE['PlayerMap']['Owner']['Shield']['CurrentCharges']
def getMaxShieldCharge():
    return STATE['PlayerMap']['Owner']['Shield']['MaxRadius']
def getRandomAttacked():
    return choice(SHIPS_ATTACKED)
def getCenterAttackedShip():
    ship = getRandomAttacked()
    if ship['orientation'] == ORIENTATION_VERTICAL:
        x = ship['pivot']
        y = (ship['low_bound'] + ship['high_bound']) / 2
    else:
        x = (ship['low_bound'] + ship['high_bound']) / 2
        y = ship['pivot']
    return {'X': x, 'Y': y}
def popHitCells():
    global DATA
    return DATA['hit_cells'].pop()

def getNearCells(x, y):
    cell = []
    if x != 0 and not DIRECTION_WEST in DATA['event_hit']:
        if isNothing(x-1, y):
            cell.append({'direction': DIRECTION_WEST, 'X': (x-1), 'Y': y})
    if x != MAP_SIZE-1 and not DIRECTION_EAST in DATA['event_hit']:
        if isNothing(x+1, y):
            cell.append({'direction': DIRECTION_EAST, 'X': (x+1), 'Y': y})
    if y != 0 and not DIRECTION_SOUTH in DATA['event_hit']:
        if isNothing(x, y-1):
            cell.append({'direction': DIRECTION_SOUTH, 'X': x, 'Y': (y-1)})
    if y != MAP_SIZE-1 and not DIRECTION_NORTH in DATA['event_hit']:
        if isNothing(x, y+1):
            cell.append({'direction': DIRECTION_NORTH, 'X': x, 'Y': (y+1)})

    return cell

def isWarPhase():
    return STATE['Phase'] == 2
def isPlacementPhase():
    return not isWarPhase()
def isDestroyed():
    return DESTROYED
def isDamaged(x, y):
    return BATTLE_MAP[x][y] == '*'
def isMissed(x, y):
    return BATTLE_MAP[x][y] == '!'
def isNothing(x, y):
    return BATTLE_MAP[x][y] == '~'
def isLastShotMiss():
    return MISSED
def isReversed():
    return DATA['reversed']
def isAttacked():
    return len(SHIPS_ATTACKED) > 0
def isShieldActive():
    return STATE['PlayerMap']['Owner']['Shield']['Active'] 

def loadData():
    global DATA, ENEMY_SHIPS, DESTROYED, MISSED, PREVIOUS_CELL, PREP_CELL
    with open("data.json", "r") as file:
        DATA = json.load(file)

    gatherShipsInfo()

    PREP_CELL = DATA['prep_cell']
    PREVIOUS_CELL = DATA['previous_cell']
    if DATA['previous_cell'] != None:
        prevCell = DATA['previous_cell']
        x = prevCell['X']
        y = prevCell['Y']
        MISSED = isMissed(x, y)
        if DATA['enemy_ships'] > ENEMY_SHIPS:
            DESTROYED = True
            DATA['enemy_ships'] = ENEMY_SHIPS

    if PREVIOUS_CELL != None:
        countPrevFireArea()
        countPrevFireDamaged()
        setPrepCell()
        collectHitCell()

def countPrevFireArea():
    global FIRE_COUNT
    fire = getFireType()
    if fire == FIRE_SINGLE:
        FIRE_COUNT = 1
    elif fire == FIRE_DOUBLE_VER or fire == FIRE_DOUBLE_HOR:
        FIRE_COUNT = 2
    elif fire == FIRE_CROSS_PLUS:
        FIRE_COUNT = 3

def countPrevFireDamaged():
    global FIRE_DAMAGED
    direction = getDirection()
    fire = getFireType()

    x = getPrevX()
    y = getPrevY()

    if fire == FIRE_SINGLE:
        if isDamaged(x, y):
            FIRE_DAMAGED = 1
    elif fire == FIRE_DOUBLE_VER:
        if direction == DIRECTION_NORTH:
            if isDamaged(x, y-1):
                FIRE_DAMAGED = FIRE_DAMAGED + 1
                if isDamaged(x, y+1):
                    FIRE_DAMAGED = FIRE_DAMAGED + 1
        elif direction == DIRECTION_SOUTH:
            if isDamaged(x, y+1):
                FIRE_DAMAGED = FIRE_DAMAGED + 1
                if isDamaged(x, y-1):
                    FIRE_DAMAGED = FIRE_DAMAGED + 1
    elif fire == FIRE_DOUBLE_HOR:
        if direction == DIRECTION_EAST:
            if isDamaged(x-1, y):
                FIRE_DAMAGED = FIRE_DAMAGED + 1
                if isDamaged(x+1, y):
                    FIRE_DAMAGED = FIRE_DAMAGED + 1
        elif direction == DIRECTION_WEST:
            if isDamaged(x+1, y):
                FIRE_DAMAGED = FIRE_DAMAGED + 1
                if isDamaged(x-1, y):
                    FIRE_DAMAGED = FIRE_DAMAGED + 1
    elif fire == FIRE_CROSS_PLUS:
        if direction == DIRECTION_NORTH or direction == DIRECTION_SOUTH:
            if direction == DIRECTION_NORTH:
                sa, sb, sc = y-1, y+1, 1
            elif direction == DIRECTION_SOUTH:
                sa, sb, sc = y+1, y-1, -1
            for i in range(sa, sb+sc, sc):
                if isDamaged(x, i):
                    FIRE_DAMAGED = FIRE_DAMAGED + 1
        else:
            if direction == DIRECTION_WEST:
                sa, sb, sc = x+1, x-1, -1
            elif direction == DIRECTION_EAST:
                sa, sb, sc = x-1, x+1, 1
            for i in range(sa, sb+sc, sc):
                if isDamaged(x, y):
                    FIRE_DAMAGED = FIRE_DAMAGED + 1

def setPrepCell():
    global PREP_CELL
    if FIRE_COUNT == FIRE_DAMAGED:
        fire = getFireType()
        direction = getDirection()
        cell = PREVIOUS_CELL
        x = cell['X']
        y = cell['Y']
        if fire == FIRE_CROSS_PLUS or fire == FIRE_DOUBLE_VER or fire == FIRE_DOUBLE_HOR:
            if direction == DIRECTION_NORTH:
                y = y + 1
            elif direction == DIRECTION_SOUTH:
                y = y - 1
            elif direction == DIRECTION_EAST:
                x = x + 1
            elif direction == DIRECTION_WEST:
                x = x - 1
            c = x, y
            PREP_CELL = c
            return
    PREP_CELL = None

def collectHitCell():
    global DATA
    fire, direction = getFireType(), getDirection()
    x, y = getPrevX(), getPrevY()
    hit_cells = []
    if fire == FIRE_CROSS_DIA:
        hit_cells.extend(crossDiaHit(x, y))
    elif fire == FIRE_MISSILE:
        hit_cells.extend(missileHit(x, y))
    elif fire == FIRE_CROSS_PLUS:
        hit_cells.extend(crossPlusHit(x, y, direction))
    elif fire == FIRE_DOUBLE_VER:
        hit_cells.extend(doubleVerHit(x, y, direction))
    elif fire == FIRE_DOUBLE_HOR:
        hit_cells.extend(doubleHorHit(x, y), direction)
    elif fire == FIRE_CORNER:
        hit_cells.extend(cornerHit(x, y))

    DATA['hit_cells'].extend(hit_cells)

def cornerHit(x, y):
    hit_cells = []
    if isDamaged(x-1, y-1):
        hit_cells.append({'X': x-1, 'Y': y})
    if isDamaged(x-1, y+1):
        hit_cells.append({'X': x-1, 'Y': y+1})
    if isDamaged(x+1, y-1):
        hit_cells.append({'X': x+1, 'Y': y-1})
    if isDamaged(x+1, y+1):
        hit_cells.append({'X': x+1, 'Y': x+1})
    return hit_cells

def missileHit(x, y):
    hit_cells = []
    if isNothing(x, y):
        snap = DATA['snap']
        for i in range(x-2, x+2):
            for j in range(y-2, y+2):
                if BATTLE_MAP[i][j] != snap[i-(x-2)][j-(y-2)]:
                    hit_cells.append({'X': i, 'Y': j})
                    break
    elif isDamaged(x, y):
        hit_cells.append({'X': x, 'Y': y})
    return hit_cells

def crossPlusHit(x, y, direction):
    if direction == DIRECTION_NORTH or direction == DIRECTION_SOUTH:
        if isDamaged(x-1, y):
            hit_cells.append({'X': x-1, 'Y': y})
        if isDamaged(x+1, y):
            hit_cells.append({'X': x+1, 'Y': y})
        if direction == DIRECTION_NORTH:
            if isMissed(x, y-1):
                if isDamaged(x, y):
                    hit_cells.append({'X': x, 'Y': y})
                    hit_cells.append({'X': x, 'Y': y+1})
            elif isMissed(x, y):
                if isDamaged(x, y+1):
                    hit_cells.append({'X': x, 'Y': y+1})
        if direction == DIRECTION_SOUTH:
            if isMissed(x, y+1):
                if isDamaged(x, y):
                    hit_cells.append({'X': x, 'Y': y})
                    hit_cells.append({'X': x, 'Y': y-1})
            elif isMissed(x, y):
                if isDamaged(x, y-1):
                    hit_cells.append({'X': x, 'Y': y-1})
    else:
        if isDamaged(x, y-1):
            hit_cells.append({'X': x, 'Y': y-1})
        if isDamaged(x, y+1):
            hit_cells.append({'X': x, 'Y': y+1})
        if direction == DIRECTION_WEST:
            if isMissed(x+1, y):
                if isDamaged(x, y):
                    hit_cells.append({'X': x, 'Y': y})
                    hit_cells.append({'X': x-1, 'Y': y})
            elif isMissed(x, y):
                if isDamaged(x-1, y):
                    hit_cells.append({'X': x-1, 'Y': y})
        if direction == DIRECTION_EAST:
            if isMissed(x-1, y):
                if isDamaged(x, y):
                    hit_cells.append({'X': x, 'Y': y})
                    hit_cells.append({'X': x+1, 'Y': y})
            elif isMissed(x, y):
                if isDamaged(x+1, y):
                    hit_cells.append({'X': x+1, 'Y': y})
def crossDiaHit(x, y):
    hit_cells = []
    if isDamaged(x, y):
        hit_cells.append({'X': x, 'Y': y})
    if isDamaged(x-1, y-1):
        hit_cells.append({'X': x-1, 'Y': y})
    if isDamaged(x-1, y+1):
        hit_cells.append({'X': x-1, 'Y': y+1})
    if isDamaged(x+1, y-1):
        hit_cells.append({'X': x+1, 'Y': y-1})
    if isDamaged(x+1, y+1):
        hit_cells.append({'X': x+1, 'Y': x+1})
    return hit_cells

def doubleVerHit(x, y, direction):
    hit_cells = []
    if direction == DIRECTION_NORTH:
        if isDamaged(x, y+1):
            hit_cells.append({'X': x, 'Y': y+1})
    elif direction == DIRECTION_SOUTH:
        if isDamaged(x, y-1):
            hit_cells.append({'X': x, 'Y': y-1})
    return hit_cells

def doubleHorHit(x, y, direction):
    if direction == DIRECTION_WEST:
        if isDamaged(x-1, y):
            hit_cells.append({'X': x-1, 'Y': y})
    elif direction == DIRECTION_EAST:
        if isDamaged(x+1, y):
            hit_cells.append({'X': x+1, 'Y': y})

def readMap():
    global BATTLE_MAP
    opponent_map = STATE['OpponentMap']

    for cell in opponent_map['Cells']:
        if cell['Y'] == 0:
            column = []

        if cell['Damaged']:
            column.append('*')
        elif cell['Missed']:
            column.append('!')
        else:
            column.append('~')

        if cell['Y'] == (MAP_SIZE-1):
            BATTLE_MAP.append(column)

def checkPlayerShips():
    global MAX_ENERGY_SAVING
    player = STATE['PlayerMap']
    m = 0
    for ship in player['Owner']['Ships']:
        weapon = ship['Weapons'][1]
        name = ship['ShipType']
        if not ship['Destroyed'] and weapon['EnergyRequired'] > m:
            m = weapon['EnergyRequired']
        ship[name] = not ship['Destroyed'] and weapon['EnergyRequired'] <= player['Owner']['Energy']
    MAX_ENERGY_SAVING = m

def gatherShipsInfo():
    global SHIPS_INFO, SHIPS_ATTACKED

    for i in range(0, 5):
        SHIPS_INFO[i]['orientation'] = DATA['ships'][i]['orientation']
        SHIPS_INFO[i]['low_bound'] = DATA['ships'][i]['low_bound']
        SHIPS_INFO[i]['high_bound'] = DATA['ships'][i]['high_bound']
        SHIPS_INFO[i]['pivot'] = DATA['ships'][i]['pivot']

    for ship in SHIPS_INFO:
        health = 0
        for i in range(ship['low_bound'], ship['high_bound']+1):
            if ship['orientation'] == ORIENTATION_HORIZONTAL:
                if not isDamaged(ship['pivot'], i):
                    health = health + 1
            else:
                if not isDamaged(i, ship['pivot']):
                    health = health + 1
        if ship['health'] > health:
            ship['attacked'] = True
            ship['health'] = health
            SHIPS_ATTACKED.append(ship)
        else:
            ship['attacked'] = False


def checkOpponentShips():
    global ENEMY_SHIPS
    opponent = STATE['OpponentMap']
    for ship in opponent['Ships']:
        if not ship['Destroyed']:
            ENEMY_SHIPS = ENEMY_SHIPS + 1

def initData():
    global SHIPS_CONFIG, SHIPS_INFO

    map_size = getMapSize()
    available_cluster = [];
    if map_size == 7:
        cluster = small_cluster;
        SHIPS_CONFIG = ships_small
        ship_info = ships_info_small
    elif map_size == 10:
        cluster = medium_cluster;
        SHIPS_CONFIG = ships_med
        ship_info = ships_info_med
    elif map_size == 14:
        cluster = large_cluster;
        SHIPS_CONFIG = ships_large
        ship_info = ships_info_large
    for i in range(len(cluster)):
        available_cluster.append(i);

    for i in range(0, 5):
        SHIPS_INFO[i]['orientation'] = ship_info[i]['orientation']
        SHIPS_INFO[i]['low_bound'] = ship_info[i]['low_bound']
        SHIPS_INFO[i]['high_bound'] = ship_info[i]['high_bound']
        SHIPS_INFO[i]['pivot'] = ship_info[i]['pivot']

    data = {
        "available_cluster": available_cluster,
        "past_cluster": [],
        "previous_cell": None,
        "predicted_cell": None,
        "cluster": cluster,
        "enemy_ships": 5,
        "fire_direction": None,
        "previous_event": 0,
        "fire_type": 0,
        "hit_cell": None,
        "event_hit": [],
        "reversed": False,
        "fire_type": None,
        "prep_cell": None,
        "hit_cells": [],
        "snap": [],
        "ships": SHIPS_INFO
    }

    file = open("data.json", "w");
    file.write(json.dumps(data));
    file.close();

def finish():
    global DATA
    DATA['previous_cell'] = PREVIOUS_CELL
    DATA['prep_cell'] = PREP_CELL
    DATA['ships'] = SHIPS_INFO
    file = open("data.json", "w");
    file.write(json.dumps(DATA));
    file.close();

def printMap():
    for row in BATTLE_MAP:
        print row

def logging(s):
    file = open("log.dat", "a");
    s = "DATA: " + s + "\n";
    file.write(s);
    file.close();

def test():
    print json.dumps(STATE, indent=4, separators=(',', ': '))
    print json.dumps(DATA, indent=4, separators=(',', ': '))
    printMap()