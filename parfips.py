from bs4 import BeautifulSoup as BS
import requests


class GetHTML:
    '''
    Класс создает объект soup по номеру товарного знака
    '''
    page_soup = None

    def __init__(self, number: int) -> None:
        try:
            self.html = requests.get(
                f'https://www1.fips.ru/registers-doc-view/fips_servlet?DB=RUTM&DocNumber={number}&TypeFile=html')
        except requests.exceptions.ConnectionError:
            self.html = 'Невозможно подключиться к реестру ФИПС'
            print(self.html)

    def get_soup(self):
        if isinstance(self.html, requests.models.Response):
            self.page_soup = BS(self.html.content, 'html.parser')


class TMData:
    def __init__(self, number):
        self.number = number

        self.html = GetHTML(self.number)
        self.html.get_soup()

    def get_img_link(self):  # -> str Возвращает ссылку на изображение товарного знака
        for i in self.html.page_soup.find_all('a', target='_blank'):
            if 'jpg' in i.get('href').lower():
                return i.get('href')

        # return [c for c in self.html.page_soup.find_all('a', target='_blank')][4].get('href')

    def get_application_date(self):
        for info in self.html.page_soup.find('td', id='BibR').find_all('p'):
            if '(220)' in info.text:
                return info.text.strip()[6:]

    def get_registration_date(self):
        for info in self.html.page_soup.find('td', id='BibR').find_all('p'):
            if '(151)' in info.text:
                return info.text.strip()[6:]

    def get_holder(self):
        temp = []
        for info in self.html.page_soup.find_all('p', class_='bib'):
            if '(732)' in info.text:
                temp.append(info.text.strip())
        return temp[-1][6:].replace('\n\n', ' ')

    def get_classes(self):
        all_p_tag = self.html.page_soup.find_all('p', class_='bib')
        classes = [goods.text.split('.')[0].replace('\n\t\t\t', '') for goods in [c for c in all_p_tag if '(511)' in c.text][0].find_all('b')]
        classes_short = []

        for mktu in classes:
            classes_short.append(mktu[:2])

        return classes, classes_short

    def unprotected(self):
        for info in self.html.page_soup.find_all('p', class_='bib'):
            if '(526)' in info.text:
                return info.text.strip()[6:].split('\n')[2]

