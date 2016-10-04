"""
    KLADR parser
        loads all russian regions, then for each region loads cities in this area
        save into json file for future processing
"""

from lxml import html
import requests
import json
import codecs

VERBOSE = False
URL = 'http://kladr-rf.ru/'
OUT = 'cities.json'


def get_regions():
    page = requests.get(URL)
    tree = html.fromstring(page.content)

    regions = tree.xpath('/html/body/div[2]/div[3]/.//a/text()')
    codes = tree.xpath('/html/body/div[2]/div[3]/.//span/text()')

    result = []
    for item in zip(regions, codes):
        if VERBOSE:
            print('{}: {}'.format(item[1], item[0]))
        result.append({'code': item[1], 'name': item[0]})

    return result

def get_cities_for_region(reg_code):
    reg_url = URL + reg_code
    page = requests.get(reg_url)
    tree = html.fromstring(page.content)

    cities = tree.xpath('/html/body/div[2]/div[6]/.//a/text()')
    cleaned = []
    for city in cities:
        city = city.lower().replace('город', '').strip().capitalize()
        cleaned.append(city)

    if VERBOSE:
        for c in cleaned:
            print('\t\t{}'.format(city))

    return cleaned

def save_json(data):
    f = codecs.open(OUT, 'w', 'utf-8')
    f.write(json.dumps(data, ensure_ascii=False))
    f.close()

def main():
    regions = get_regions()
    for region in regions:
        if region['code'] != '99':  # skip for Baikonur
            cities = get_cities_for_region(region['code'])
            region['cities'] = cities

    save_json(regions)

if __name__ == '__main__':
    main()
