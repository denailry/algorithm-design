import argparse
import json
import os
from random import choice
import event_manager as mEvent
import attack_manager as mAttack
import data_manager as mData

FILE_COMMAND = "command.txt"
FILE_PLACEMENT = "place.txt"
FILE_STATE = "state.json"
PATH_OUTPUT = '.'

def main(key):
    with open(os.path.join(PATH_OUTPUT, FILE_STATE), 'r') as f_in:
        mData.setState(json.load(f_in))

    if mData.isPlacementPhase():
        clearLog()
        mData.initData()
        place_ships()
    else:
        mData.loadData()
        mAttack.setPath(os.path.join(PATH_OUTPUT, FILE_COMMAND))
        mEvent.start()
        mData.finish()

def logging(s):
    file = open("log.dat", "a");
    s = "MAIN: " + s + "\n";
    file.write(s);
    file.close();

def place_ships():
    ships = mData.SHIPS_CONFIG
    with open(os.path.join(PATH_OUTPUT, FILE_PLACEMENT), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return

def clearLog():
    file = open("log.txt", "w");
    file.write("");
    file.close();

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    PATH_OUTPUT = args.WorkingDirectory
    main(args.PlayerKey)
