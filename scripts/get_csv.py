import sys
import requests


if __name__ == "__main__":
    url = 'http://cms.qobit.co/get_csv?ex={}&timeframe={}&start={}&end={}'
    if len(sys.argv) < 4:
        print ('Please provide valid parameraters.\ne.g)$python get_csv.py binance 1min 1402197000 1402197180')
        exit(0)

    url = url.format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    info = requests.get(url)
    file_path = '{}-{}.csv'.format(sys.argv[1], sys.argv[3])

    with open(file_path, "wb") as file:
        file.write(info.content)
