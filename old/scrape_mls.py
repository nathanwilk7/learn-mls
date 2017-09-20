from subprocess import call
import time

start = 0
end_exclusive = 9999999
url = 'https://www.audi-player-index.com/en/getMatch/{_id}/latest/'
_dir = 'matches'
curl_cmd = 'curl {url} > {_dir}/{filename}'
filename = '{_id}.json'
printerval = 100

for _id in range(start, end_exclusive, 1):
    if _id % printerval == 0:
        print(_id)
    temp_url = url.format(_id=_id)
    temp_filename = filename.format(_id=_id)
    temp_curl_cmd = curl_cmd.format(url=temp_url, _dir=_dir, filename=temp_filename)
    call(temp_curl_cmd, shell=True)
    time.sleep(1)

{"status":"success","match":{"players":[],"snapshots":[],"range":{"from":null,"till":null}}}
