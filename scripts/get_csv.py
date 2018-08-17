import sys
import requests


if __name__ == "__main__":
    url = 'http://cms.qobit.co/get_csv?ex={}&pair={}&timeframe={}&start={}&end={}'
    # url = 'http://localhost:8000/get_csv?ex={}&pair={}&timeframe={}&start={}&end={}'

    if len(sys.argv) < 6:
        print ('Please provide valid parameraters.\ne.g)$python get_csv.py binance BTC-USDT 5M 2018-08-12T03:00 2018-08-12T13:00')
        exit(0)

    url = url.format(sys.argv[1], sys.argv[2], sys.argv[3], 
                     sys.argv[4].replace('T', ' '), 
                     sys.argv[5].replace('T', ' '))

    info = requests.get(url)
    file_path = '{}-{}-{}.csv'.format(sys.argv[1], sys.argv[2], sys.argv[4])

    with open(file_path, "wb") as file:
        file.write(info.content)
