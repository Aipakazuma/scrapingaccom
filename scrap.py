# -*- coding:utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
import sys


def get_web_resource(url):
    try:
        return urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print('The server could not be found!')
        return None


def municipality(municipality_name, url):
    resource = get_web_resource(url)
    read_resource = resource.read()
    bs_obj = BeautifulSoup(read_resource, 'lxml')

    try:
        table = bs_obj.find('div', {'id': 'sction01'}).find('table')
        school_names = table.findAll('td', {'class': 'cell2'})
        school_froms = table.findAll('td', {'class': 'cell3'})
        for school_name, school_from in zip(school_names, school_froms):
            school_name_text = school_name.find('a').getText().strip()
            school_from_text = school_from.find('p').getText().strip()
            print(municipality_name + ',' + school_name_text + ',' + school_from_text)
    except Exception as e:
        print(e)


def main(url):
    resource = get_web_resource(url)
    read_resource = resource.read()
    bs_obj = BeautifulSoup(read_resource, 'lxml')

    try:
        # linkを取得
        school_link_tds = bs_obj.find('div', {'id': 'sction01'}).find('table').findAll('td')
        for school_link_td in school_link_tds:
            school_link = school_link_td.find('a')
            municipality(municipality_name=school_link.getText().strip(), url=school_link['href'])

    except Exception as e:
        print(e)


if __name__ == '__main__':
    if 0 < len(sys.argv) <= 1:
        print('Usage: argument scraping url')
        exit()

    main(sys.argv[1])
