import requests as req
from bs4 import BeautifulSoup as bs

# https://geocode-maps.yandex.ru/1.x/?geocode=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0+%D0%9B%D1%8C%D0%B2%D0%B0+%D0%A2%D0%BE%D0%BB%D1%81%D1%82%D0%BE%D0%B3%D0%BE+16


def performRequest(address):

    payload = {}
    base = 'https://geocode-maps.yandex.ru/1.x/'
    payload['geocode'] = address
    resp = req.get(base, params = payload)
    t = resp.text
    soup = bs(t, "lxml")
    # print(soup.prettify())
    return soup


def processResponse(soup):

    all_coords = []
    places = soup.find_all('featuremember')
    for p in places:
        pos = p.find('point').find('pos')
        pos_txt = pos.text
        str_coords = pos_txt.split(' ')
        coords = [float(i) for i in str_coords][::-1]
        all_coords.append(coords)

    return all_coords[0]


# "Latitude","Longitude","Description","Label","Placemark number"
# 66.110556,-162.680278,"Enable sattelite layer to see the blue ice of Kotzebue Sound; Northwest Arctic, Alaska, United States","Kotzebue Sound",1
# 71.254353,137.7154199,"Enable sattelite layer to see the great delta of the Yana river; Sakha Republic, Russian Federation","Yana Bay",2
# 25.504444,-97.999722,"Enable sattelite layer to see the geometry of Rio Grande; Tamaulipas, Mexico","Rio Grande",3
# 36.060833,-101.750556,"Enable sattelite layer to see the round fields of Sherman; Texas, United States","Sherman",4
    

def main():

    uploadable = open('uploadable.csv', 'w', encoding='utf8')

    addresses = open('addresses', 'r', encoding='utf8')
    for line in addresses:
        soup = performRequest(line)
        processResponse(soup)

    addresses.close()
    uploadable.close()    


if __name__ == '__main__':
    main()