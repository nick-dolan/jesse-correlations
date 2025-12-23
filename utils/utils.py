import datetime
from pathlib import Path


def generate_file(result):
    with open('sample.html', 'r') as file:
        file_data = file.read()

    title = f"Correlation Table ◾ {datetime.datetime.today().strftime('%d %b, %Y %H:%M')}"

    file_data = file_data \
        .replace('#DATE', title) \
        .replace('#JSON', result)

    Path("./storage/correlations").mkdir(parents=True, mode=0o777, exist_ok=True)

    file_name = "storage/correlations/correlation__{}.html".format(datetime.datetime.today().strftime("%Y-%m-%d__%H-%M"))

    with open(file_name, 'w') as file:
        file.write(file_data)