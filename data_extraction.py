"""
Extract Christie's art sale data.

Scrape Christie's website to get sale information for Nov. 2017 and
Mar. 2018 auctions. Saves a csv in the root directory for each sale.
"""

import requests

from bs4 import BeautifulSoup, element
import pandas as pd

from config import URL_NOV_2017_SALE, URL_MAR_2018_SALE, NOV_2017_SALE_DATA_CSV, \
    MAR_2018_SALE_DATA_CSV


def get_data_from_table_row(html_row: element.Tag) -> dict:
    """Return art lot data from HTML table row."""
    lot_info = html_row.find('td', 'lot-info')
    price_info = html_row.find('td', 'estimate').findAll('span', 'lot-description')
    return {
        'lot_number': lot_info.find('span', 'lot-number').text,
        'artist_description': lot_info.find('span', 'lot-description').text,
        'title': lot_info.find('span', 'lot-maker').text,
        'medium_dimensions': lot_info.find('span', 'medium-dimensions').text,
        'price_estimate': price_info[0].text if len(price_info) == 2 else None,
        'price_realized': price_info[1].text if len(price_info) == 2 else None,
    }


def extract_data(source_url: str):
    """Extract data from source URL as dataframe."""
    result = requests.get(source_url)
    html_content = result.content
    html_content_parsed = BeautifulSoup(html_content, 'lxml')
    data_table_rows = html_content_parsed.findAll('tr')[1:]  # first row has no data so ignore it
    data = [get_data_from_table_row(row) for row in data_table_rows]
    return pd.DataFrame(data)

if __name__ == '__main__':
    NOV_2017_DATA = extract_data(URL_NOV_2017_SALE)
    MAR_2018_DATA = extract_data(URL_MAR_2018_SALE)
    NOV_2017_DATA.to_csv(NOV_2017_SALE_DATA_CSV, index=False)  # ignore pandas generated index
    MAR_2018_DATA.to_csv(MAR_2018_SALE_DATA_CSV, index=False)
