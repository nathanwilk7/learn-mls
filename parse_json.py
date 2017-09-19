import json

matches_path = 'matches/'
match_id = '902128'
file_ext = 'json'
with open('{matches_path}{match_id}.{file_ext}'.format(matches_path=matches_path, match_id=match_id, file_ext=file_ext), 'r') as r:
    m = json.load(r)

import pdb
pdb.set_trace()
