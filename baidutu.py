from urllib.parse import urlencode
import requests
import re
import os
save_dir='baidutu/'

def  baidtu_uncomplie(url):
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d= {'w':'a', 'k':'b', 'v':'c', '1':'d', 'j':'e', 'u':'f', '2':'g', 'i':'h', 't':'i', '3':'j', 'h':'k', 's':'l', '4':'m', 'g':'n', '5':'o', 'r':'p', 'q':'q', '6':'r', 'f':'s', 'p':'t', '7':'u', 'e':'v', 'o':'w', '8':'1', 'd':'2', 'n':'3', '9':'4', 'c':'5', 'm':'6', '0':'7', 'b':'8', 'l':'9', 'a':'0', '_z2C$q':':', '_z&e3B':'.', 'AzdH3F':'/'}
    if(url==None or 'http' in url):
        return url
    else:
        j= url
        for m in c:
            j=j.replace(m,d[m])
        for char in j:
            if re.match('^[a-w\d]+$',char):
                char = d[char]
            res= res+char
        return res

def get_page(offset):
    params = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct':'201326592',
        'is':'',
        'fp': 'result',
        'queryWord': '帅哥',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid':'',
        'st': '-1',
        'z':'',
        'ic': '0',
        'word': '帅哥',
        's':'',
        'se':'',
        'tab':'',
        'width':'',
        'height':'',
        'face': '0',
        'istype': '2',
        'qc':'',
        'nc': '1',
        'fr':'',
        'expermode':'',
        'pn': offset*30,
        'rn': '30',
        'gsm': '1e',
        '1537355234668':'',
    }
    url = 'https://image.baidu.com/search/acjson?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('fromPageTitle'):
                title = item.get('fromPageTitle')
            else:
                title='noTitle'
            image = baidtu_uncomplie(item.get('objURL'))
            if(image):
                yield {
                    'image': image,
                    'title': title
                }

def save_image(item,count):
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = save_dir+'{0}.{1}'.format(str(count), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

def main(pageIndex,count):
    json = get_page(pageIndex)
    for image in get_images(json):
        save_image(image, count)
        count += 1
    return count
if __name__=='__main__':
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    count=1
    for i in range(1,20):
        count=main(i,count)
    print('total:',count)
