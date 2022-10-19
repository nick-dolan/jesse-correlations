import threading
import time
import sys

from config import config

import numpy as np
import itertools
from jesse import research
import json
import datetime
from pathlib import Path

pairs = config['pairs']
exchange = config['exchange']
start_date = config['corr_start_date']
finish_date = config['corr_finish_date']
timeframe = config['timeframe']

done = False

def animate():
    for c in itertools.cycle(['', '.', '..', '...']):
        if done:
            break

        sys.stdout.write('\rCalculating correlations' + c)
        sys.stdout.flush()
        time.sleep(0.5)

    sys.stdout.write('\rDone!')


t = threading.Thread(target=animate)
t.start()

#
# Calculate correlation
#
count = len(pairs)

grid = np.ones(shape=(count, count))

for (i, first), (j, second) in itertools.combinations(enumerate(pairs), 2):
    try:
        first_candles = research.get_candles(exchange, first, timeframe, start_date, finish_date)
        second_candles = research.get_candles(exchange, second, timeframe, start_date, finish_date)
    except Exception as e:
        print("An exception occurred")
        print(e)
        break

    res = np.corrcoef(first_candles[:, -1], second_candles[:, -1])

    grid[i, j], grid[j, i] = res[0, 1], res[1, 0]

metadata = {
    "pairs": list(map(lambda item: item.replace('-', '/'), pairs)),
    "exchange": exchange,
    "timeframe": timeframe,
    "start_date": start_date.replace('-', '.'),
    "finish_date": finish_date.replace('-', '.'),
}

#
# Generate html output
#
result = {'grid': grid.tolist(), 'metadata': metadata}
result = json.dumps(result)

with open('sample.html', 'r') as file:
    file_data = file.read()
title = "Correlation Table ◾ {}".format(datetime.datetime.today().strftime("%d %b, %Y %H:%M"))

file_data = file_data \
    .replace('#DATE', title) \
    .replace('#JSON', result)

Path("./storage/correlations").mkdir(parents=True, mode=0o777, exist_ok=True)

file_name = "storage/correlations/correlation__{}.html".format(datetime.datetime.today().strftime("%Y-%m-%d__%H-%M"))

with open(file_name, 'w') as file:
    file.write(file_data)

done = True