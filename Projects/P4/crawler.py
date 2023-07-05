from urllib.request import urlopen
from xml.etree.ElementTree import fromstring

if __name__ == '__main__':
    sum = 0
    url = 'http://py4e-data.dr-chuck.net/comments_1109463.xml'
    uh = urlopen(url)
    fhand = uh.read()
    datas = fromstring(fhand)
    lst = datas.findall('comments/comment/count')
    for item in lst:
        num = int(item.text)
        sum += num
    print(sum)
