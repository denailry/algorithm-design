import data_manager as mData
from random import choice
import event_manager as mEvent

PATH = None

arr_strike = [mData.FIRE_CROSS_PLUS, mData.FIRE_DOUBLE_VER, mData.FIRE_SINGLE, mData.FIRE_NOTHING]
arr_random = [mData.FIRE_CROSS_DIA, mData.FIRE_MISSILE, mData.FIRE_CORNER, mData.FIRE_SINGLE, mData.FIRE_NOTHING]

def setPath(path):
    global PATH
    PATH = path

def nearShot():
    nearCell = mData.getNearCells(mData.getPrevX(), mData.getPrevY())
    if len(nearCell) == 0:
        mEvent.event_handler(mEvent.EVENT_NONE)
        return
    cell = choice(nearCell)
    mData.addEventHit(cell)
    x = cell['X']
    y = cell['Y']
    mData.setPredictedCell(x, y)
    output_shot(mData.FIRE_SINGLE, x, y)

def strike():
    direction = mData.getDirection()
    fire = mData.getFireType()
    x = mData.getPrevX()
    y = mData.getPrevY()
    if fire == mData.FIRE_DOUBLE_VER or fire == mData.FIRE_DOUBLE_HOR:
        if mData.FIRE_DAMAGED == 0:
            mData.reverseDirection()
            mData.setFireType(mData.FIRE_SINGLE)
        elif mData.FIRE_DAMAGED == 1:
            mData.reverseDirection()
            output_shot(mData.FIRE_SINGLE, x, y)
            return
        elif mData.FIRE_DAMAGED == 2:
            output_shot(mData.FIRE_SINGLE, x, y)
            mData.setPrevCell(mData.PREP_CELL)
            return
    if fire == mData.FIRE_CROSS_PLUS:
        if mData.FIRE_COUNT == mData.FIRE_DAMAGED:
            mData.setPrevCell(mData.PREP_CELL)
        else:
            mData.reverseDirection()

    fire = 0
    while(fire == 0):
        fire = greedy_fire(mData.setNextX(fire, direction, x), mData.setNextY(fire, direction, y), arr_strike)
        if fire == 0:
            if not mData.isReversed():
                mData.reverseDirection()
            else:
                mData.clearHitCell()
                mEvent.event_handler(mEvent.EVENT_NONE)
                return

    if fire == 2 and (direction == mData.DIRECTION_WEST or direction == mData.DIRECTION_EAST):
        fire = 3 

    x = mData.setNextX(fire, mData.getDirection(), x)
    y = mData.setNextY(fire, mData.getDirection(), y)
    c = x, y
    mData.setPrevCell(c)
    output_shot(fire, x, y)

def greedy_fire(x, y, arr):
    fire_array = arr
    for fire in fire_array:
        if fire == 0:
            return fire
        c1 = mData.checkAvailability(fire)
        c2 = mData.checkSpace(fire, x, y)
        if c1 and c2:
            return fire

def randomShot():
    targets = [];

    available_cluster = mData.getAvailCluster()
    past_cluster = mData.getPastCluster()
    cluster = mData.getCluster()

    while len(targets) == 0:
        if len(available_cluster) == 0:
            for index in past_cluster:
                available_cluster.append(index);
            past_cluster = [];

        index = choice(available_cluster);
        available_cluster.remove(index);

        lRow = cluster[index]["lRow"];
        hRow = cluster[index]["hRow"];
        lCol = cluster[index]["lCol"];
        hCol = cluster[index]["hCol"];

        for x in range(lRow, hRow+1):
            for y in range(lCol, hCol+1):
                if mData.isNothing(x, y):
                    valid_cell = {'X': x, 'Y': y}
                    targets.append(valid_cell)

    past_cluster.append(index);
    target = choice(targets);
    x = target['X']
    y = target['Y']

    if mData.getPlayerEnergy() >= 2 * mData.MAX_ENERGY_SAVING:
        fire = greedy_fire(x, y, arr_random)
        if fire == 0:
            fire = mData.FIRE_SINGLE
    else:
        fire = mData.FIRE_SINGLE

    output_shot(fire, x, y)

    mData.setAvailCluster(available_cluster)
    mData.setPastCluster(past_cluster)
    mData.setPrevCell(target)

    return

def activate_shield():
    cell = mData.getCenterAttackedShip()
    output_shot(mData.ACTIVATE_SHIELD, cell['X'], cell['Y'])

def output_shot(move, x, y):
    global PATH
    mData.setFireType(move)
    with open(PATH, 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def logging(s):
    file = open("log.dat", "a");
    s = "ATTACK: " + s + "\n";
    file.write(s);
    file.close();

def test():
    mData.test()