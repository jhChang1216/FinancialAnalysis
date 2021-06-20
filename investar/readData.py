from bs4 import BeautifulSoup
import requests
import pandas as pd

def read_per_page(url, page):
    page_url = '{}&page={}'.format(url, page)
    req = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
    page_data = BeautifulSoup(req, 'lxml')

    num_extr = page_data.find_all('td', class_='num')
    table_header = page_data.find_all('th')
    dates = page_data.find_all('span', attrs={'class': 'tah p10 gray03'})

    columns = list(range(len(table_header)))
    index = list(range(len(dates)))
    rows = []
    rows_buffer = []

    for i in range(len(table_header)):
        columns[i] = table_header[i].text

    for i in range(len(dates)):
        index[i] = dates[i].text

    for i in range(0, len(num_extr), 6):
        if num_extr[i].text == '\xa0':
            break
        for j in range(6):
            if j % 6 == 1:
                pure_num = num_extr[i + j].text
                pure_num = pure_num.replace('\t', '').replace('\n', '')
                rows_buffer.append(int(pure_num.replace(',', '')))
                continue
            rows_buffer.append(int(num_extr[i + j].text.replace(',', '')))
        rows.append(rows_buffer)
        rows_buffer = []

    data_per_page = pd.DataFrame(rows, columns=columns[1:], index=index)
    return data_per_page

def read_total_data(url, last_page, pages_to_fetch):
    total_data = pd.DataFrame()

    pages = min(int(last_page), pages_to_fetch)

    for page in range(0, pages + 1):
        data_per_page = read_per_page(url, page)
        total_data = total_data.append(data_per_page)
    return total_data