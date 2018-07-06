import md5
import urllib
import random
import requests

appKey = '1715fb676662d600'
secretKey = 'h3GEsGNxQE0ATTXYNs3JbDGbfN9s0R1X'

def translate(q, fromLang='EN', toLang='zh-CHS'):
    salt = random.randint(1, 65536)
    sign = appKey+q+str(salt)+secretKey

    m1 = md5.new()
    m1.update(sign)

    url = 'https://openapi.youdao.com/api?appKey='+appKey+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+m1.hexdigest()
     
    try:
        info = requests.get(url).json()
        return info['translation'][0].encode('utf-8').split('\n')
    except:
        pass
    return ['', '']
