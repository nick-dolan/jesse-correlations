import itertools
import threading
import time
import sys

from config import config

from jesse import research

exchange = config['exchange']
start_date = config['import_start_date']
pairs = config['pairs']
current_pair = ''
done = False


def animate():
    for c in itertools.cycle(['', '.', '..', '...']):
        if done:
            break

        sys.stdout.write('\rImporting ' + current_pair + c)
        sys.stdout.flush()
        time.sleep(0.5)

    sys.stdout.write('\rDone!')


t = threading.Thread(target=animate)
t.start()

for pair in pairs:
    current_pair = pair

    try:
        research.import_candles(exchange, pair, start_date, show_progressbar=False)
    except Exception as e:
        print("An exception occurred")
        print(e)
        continue

done = True
