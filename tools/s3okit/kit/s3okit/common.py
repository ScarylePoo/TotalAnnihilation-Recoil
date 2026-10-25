import os
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.environ.get('S3OKIT_WORK', os.path.join(KIT, 'work'))
REPO = os.environ.get('XTA_REPO', '/home/claude/xta-springrts')

# Material slots. Every mesh uses this list in this order; the bake encodes the slot index.
MATS = ['paint', 'paint2', 'dark', 'tread', 'steel', 'team', 'lightw', 'lightc', 'lightr',
        'black', 'hazard', 'glass', 'rust', 'ash']

def workdir(name):
    d = os.path.join(WORK, name)
    os.makedirs(os.path.join(d, 'out'), exist_ok=True)
    os.makedirs(os.path.join(d, 'prev'), exist_ok=True)
    return d
