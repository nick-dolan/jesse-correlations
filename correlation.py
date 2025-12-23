import itertools
import json

import jesse.helpers as jh
import numpy as np
from jesse import research

from config import config
from utils.utils import generate_file

pairs = config['pairs']
exchange = config['exchange']
start_date = config['corr_start_date']
finish_date = config['corr_finish_date']
timeframe = config['timeframe']


print("Calculating correlations...")

#
# Calculate correlation
#
count = len(pairs)

grid = np.ones(shape=(count, count))

for (i, first), (j, second) in itertools.combinations(enumerate(pairs), 2):
    try:
        first_candles = research.get_candles(exchange, first, timeframe, jh.date_to_timestamp(start_date), jh.date_to_timestamp(finish_date))
        second_candles = research.get_candles(exchange, second, timeframe, jh.date_to_timestamp(start_date), jh.date_to_timestamp(finish_date))
    except Exception as e:
        print("An exception occurred")
        print(e)
        break


    res = np.corrcoef(first_candles[1][:, -1], second_candles[1][:, -1])

    grid[i, j], grid[j, i] = res[0, 1], res[1, 0]

#
# Generate html output
#
metadata = {
    "pairs": list(map(lambda item: item.replace('-', '/'), pairs)),
    "exchange": exchange,
    "timeframe": timeframe,
    "start_date": start_date.replace('-', '.'),
    "finish_date": finish_date.replace('-', '.'),
}

result = {'grid': grid.tolist(), 'metadata': metadata}
result = json.dumps(result)

generate_file(result)

print("Done!")
