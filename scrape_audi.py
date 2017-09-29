#import time
import urllib.request
import json
from datetime import datetime
import os.path

start = 1100000
end = 500000
step_size = -1
url = 'https://www.audi-player-index.com/en/getMatch/{_id}/latest/'
_dir = 'matches'
dest_file = '{_dir}/{filename}'
filename = '{_id}.json'
printerval = 10000

def is_legit(r):
    try:
        j = json.loads(r)
        if j == {"status":"success","match":{"players":[],"snapshots":[],"range":{"from":None,"till":None}}}:
            return False
        elif len(j['match']['players']) == 0:
            return False
        elif len(j['match']['snapshots']) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(r, e)
        return False
try:
    num_written = 0
    for _id in range(start, end, step_size):
        if _id % printerval == 0:
            print(datetime.now().time())
            print('ID: {_id}, num_written={num_written}'.format(_id=_id, num_written=num_written))
        tempfile = dest_file.format(_dir=_dir, filename=filename.format(_id=_id))
        #    if os.path.isfile(tempfile):
        #        continue
        with urllib.request.urlopen(url.format(_id=_id)) as response:
            r = response.read()
            r = r.decode('utf-8')
            if is_legit(r):
                with open(tempfile, 'w') as w:
                    w.write(r)
                    num_written += 1
        #    time.sleep(1)
except Exception as e:
    print(e)
