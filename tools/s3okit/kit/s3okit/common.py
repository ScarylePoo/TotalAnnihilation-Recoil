import os
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.environ.get('S3OKIT_WORK', os.path.join(KIT, 'work'))
# The kit lives in <repo>/tools/s3okit/kit, so the game repo is three levels up.
REPO = os.environ.get('XTA_REPO', os.path.abspath(os.path.join(KIT, '..', '..', '..')))

# Material slots. Every mesh uses this list in this order; the bake encodes the slot index.
MATS = ['paint', 'paint2', 'dark', 'tread', 'steel', 'team', 'lightw', 'lightc', 'lightr',
        'black', 'hazard', 'glass', 'rust', 'ash',
        # frame-cycled tracks (e.g. tracks1..4 shown one at a time): tread with the link pattern a quarter, half and
        # three quarters of a link further on. Appended so existing material indices never change.
        'tread2', 'tread3', 'tread4']

def workdir(name):
    d = os.path.join(WORK, name)
    os.makedirs(os.path.join(d, 'out'), exist_ok=True)
    os.makedirs(os.path.join(d, 'prev'), exist_ok=True)
    return d
