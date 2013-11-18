# coding=utf-8
__author__ = 'seamaster :P'

import mechanize
from bs4 import BeautifulSoup


def parse_and_print(url):
    target = url

    # get that soup!
    br = mechanize.Browser()
    soup = br.open(target).read()
    soup = BeautifulSoup(soup)

    # get that row
    table = soup.find_all("table")[-1]
    rows = table.find_all('tr')[1:]

    # gun & run
    print url
    print rows
    for row in rows:
        splitrow = row.find_all("td")
        level = int(splitrow[0].get_text(strip=True))
        wood = int(splitrow[1].get_text(strip=True).replace('.',''))
        stone = int(splitrow[2].get_text(strip=True).replace('.',''))
        iron = int(splitrow[1].get_text(strip=True).replace('.',''))
        print "Level: {level}. Needs: {wood}|{stone}|{iron}".format(**locals())
    print ''


urls = ["http://help.die-staemme.de/wiki/"+e for e in ["Adelshof", "Hauptgebäude", "Kaserne", "Holzfäller"]]

for url in urls:
    parse_and_print(url)