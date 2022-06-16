from bs4 import BeautifulSoup as BS
import requests


class GetHTML:
    '''
    Класс создает объект soup по номенру товарного знака
    '''
    page_soup = None

    def __init__(self, number: int) -> None:
        try:
            self.html = requests.get(
                f'https://www1.fips.ru/registers-doc-view/fips_servlet?DB=RUTM&DocNumber={number}&TypeFile=html')
        except requests.exceptions.ConnectionError:
            self.html = 'Невозможно подключиться к реестру ФИПС'

    def get_soup(self):
        if isinstance(self.html, requests.models.Response):
            self.page_soup = BS(self.html.content, 'lxml')


class TMData:
    def __init__(self, number, classes):
        self.number = number
        self.classes = classes

        html = GetHTML(self.number)
        html.get_soup()

    def get_img_link(self):  # -> str Возвращает ссылку на изображение товарного знака
        return [c for c in html.page_soup.find_all('a', target='_blank')][4].get('href')

    def get_application_date(self):
        for info in html.page_soup.find('td', id='BibR').find_all('p'):
            if '(220)' in info:
                return info
    
    def get_registration_date(self):
        for info in html.page_soup.find('td', id='BibR').find_all('p'):
            if '(151)' in info:
                return info

    def get_holder(self):
        pass

    def get_short_classes(self):
        pass

    def get_classes(self):
        pass

    def unprotected(self):
        pass


class TradeMarkInfo(GetHTML):
    '''
    Класс взят из другого проекта. На его основе создается класс TMData. Класс будет удален при завершении написания модуля parfips.py
    '''

    def __init__(self, argument, number):
        super().__init__(argument, number)

        self.status = ''
        self.goods_and_services = []
        self.goods_and_services_short = []
        self.validity_period = ''
        self.registration_info = []
        self.notifications = []
        self.img_link = ''

    def get_info(self):
        if not self.page_soup:
            self.status = self.html
        elif not self.page_soup.find('tr', class_='Status'):
            self.status = 'Документ с данным номером не найден'
        else:
            self.status = ' '.join(self.page_soup.find('tr', class_='Status').get_text().split())
            self.img_link = [c for c in self.page_soup.find_all('a', target='_blank')][4].get('href')

            all_p_tag = self.page_soup.find_all('p', class_='bib')
            self.goods_and_services = [goods.text.split('.')[0].replace('\n\t\t\t', '') for goods in
                       [c for c in all_p_tag if '(511)' in c.text][0].find_all('b')]
            for mktu in self.goods_and_services:
                self.goods_and_services_short.append(mktu[:2])

            if self.page_soup.find('p', class_='StartIzvs'):
                self.notifications.append(self.page_soup.find('p', class_='StartIzvs').text)
                all_notifications = self.page_soup.find('p', class_='StartIzvs').find_next_siblings()
                temp = []
                for c in all_notifications:
                    row = c.text.strip()
                    if row:
                        if '\n\n' in row:
                            row = row.replace('\n\n', '\n')
                        temp.append(row)
                        if '(186)' in row:
                            self.validity_period = row
                        if 'Дата публикации' in row:
                            self.notifications.append('\n'.join(temp))
                            temp = []

            table_info = self.page_soup.find('td', id='BibL').find_all('p')
            table_info += self.page_soup.find('td', id='BibR').find_all('p')
            for info in table_info:
                if '(181)' in info.get_text().strip():
                    if not self.validity_period:
                        self.validity_period = info.get_text().strip()
                    else:
                        continue
                elif '(' not in info.get_text().strip():
                    self.registration_info.append(' ' * 10 + info.get_text().strip())
                else:
                    self.registration_info.append(info.get_text().strip())
