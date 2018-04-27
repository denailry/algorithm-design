import attack_manager as mAttack
import data_manager as mData

EVENT_NONE = 0
EVENT_DESTROYED = 1
EVENT_HIT = 2
EVENT_STRIKE = 3
EVENT_STRIKE_DOUBLE = 4
EVENT_STRIKE_REDIRECT = 5

def start():
	prevEvent = mData.getPrevEvent()
	prevCell = mData.getPrevCell()
	missing = mData.FIRE_COUNT > mData.FIRE_DAMAGED
	destroyed = mData.isDestroyed()

	if not mData.isShieldActive() and mData.isAttacked() and mData.getMaxShieldCharge() <= mData.getShieldCharge():
		mAttack.activate_shield()
		return

	if prevCell == None:
		event_handler(EVENT_NONE)
		return

	if destroyed:
		mData.clearHitCell()
		event_handler(EVENT_NONE)
		return

	if prevEvent == EVENT_NONE:
		if missing:
			event_handler(EVENT_NONE)
		else:
			event_handler(EVENT_HIT)
		return

	if prevEvent == EVENT_HIT:
		if missing:
			event_handler(EVENT_HIT)
		else:
			mData.clearPredictedCell()
			event_handler(EVENT_STRIKE)
		return

	if prevEvent == EVENT_STRIKE:
		event_handler(EVENT_STRIKE)
		return

def event_handler(event):
	mData.setEvent(event)

	if event == EVENT_NONE:
		if len(mData.getHitCells()) > 0:
			cell = mData.popHitCells()
			mData.setHitCell(cell['X'], cell['Y'])
			event_handler(EVENT_HIT)
		else:
			mAttack.randomShot()
	elif event == EVENT_HIT:
		mAttack.nearShot()
	elif event == EVENT_STRIKE:
		mAttack.strike()

def logging(s):
    file = open("log.dat", "a");
    s = "EVENT: " + s + "\n";
    file.write(s);
    file.close();