import sys
import requests


if __name__ == "__main__":
    url = 'http://cms.qobit.co/get_pairs_info?ex={}'
    if len(sys.argv) < 2:
        print ('Please provide valid parameraters.\ne.g)$python get_pairs_info.py binance')
        exit(0)

    url = url.format(sys.argv[1])
    info = requests.get(url)
    file_path = '{}-pairs.csv'.format(sys.argv[1])

    with open(file_path, "wb") as file:
        file.write(info.content)
