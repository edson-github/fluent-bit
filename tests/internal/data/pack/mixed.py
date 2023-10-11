# Fluent Bit / Pack mixed samples to JSON
# =======================================
# This script generate the JSON formatted strings for the mixed_ABC.txt samples.

import os
import json
import msgpack

def gen_json(f):
    with open(f, 'r') as raw:
        data = raw.read()
    out_mp = f"{f[:-4]}.mp"
    out_json = f"{f[:-4]}.json"

    with open(out_mp, 'w') as fmp:
        fmp.write(msgpack.packb(data))
    with open(out_json, 'w') as fjson:
        fjson.write(json.dumps(data))

for fn in os.listdir('.'):
     if not os.path.isfile(fn):
         continue

     if fn.startswith('mixed_') and fn.endswith('.txt'):
         gen_json(fn)
