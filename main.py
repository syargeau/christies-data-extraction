"""
Get artist sale to sale comparison.

Run a comparison for each artist grouping similar paintings together
based on dimensions. The definition of similar is based on user input X
when running the script, where any painting within dimensions +/- X are
considered similar. The input X is in centimeters.
"""

import re
import sys

import pandas as pd

import config


def find_dimensions(medium_dimensions: str) -> dict:
    """Extract dimensions from raw data dimension description."""
    if len(re.compile(r'cm').findall(medium_dimensions)) == 2:
        numbers = re.compile(r'([\d\.]+)\scm').findall(medium_dimensions)
        height = numbers[0]
        width = numbers[1]
    else:
        height = re.compile(r'\(([\d\.]+)').findall(medium_dimensions)[0]
        width = re.compile(r'([\d\.]+)\scm').findall(medium_dimensions)[0]
    return {'height': float(height), 'width': float(width)}


def get_usd_price(price_realized: str) -> float:
    """Get the USD price from the posted realized price."""
    price = re.sub(r'[^\d]', '', price_realized)
    if not price:
        return None
    else:
        price = float(price)
        if '£' in price_realized:
            price *= config.GBP_TO_USD_EXCHANGE_RATE
        return price


def data_prep() -> pd.DataFrame:
    """Fetch and prep data."""
    data_nov = pd.read_csv(config.NOV_2017_SALE_DATA_CSV)
    data_mar = pd.read_csv(config.MAR_2018_SALE_DATA_CSV)
    data_nov['month_year'] = '2017_11'
    data_mar['month_year'] = '2018_03'
    data = pd.concat([data_nov, data_mar], ignore_index=True)
    dimensions = pd.DataFrame(data['medium_dimensions'].apply(find_dimensions).tolist())
    data = pd.concat([data, dimensions], axis=1)
    data['price_usd'] = data['price_realized'].astype(str).apply(get_usd_price)
    return data


def find_similar_objects(data: pd.DataFrame, lot: pd.Series,
                         similarity_threshold: float) -> pd.DataFrame:
    """
    Find similar objects within data from given lot.
    
    Similar is defined by the specified similarity threshold, in which
    all similar objects are within +/- the similarity threshold.
    """
    similar_objects = data[
        (data.artist_description == lot.artist_description)
        & (
            data.width.between(
                lot.width - similarity_threshold,
                lot.width + similarity_threshold, 
                inclusive=True
            )
        )
        & (
            data.height.between(
                lot.height - similarity_threshold,
                lot.height + similarity_threshold,
                inclusive=True
            )
        )
    ]
    return similar_objects


def get_report(data: pd.DataFrame, similarity_threshold: float) -> pd.DataFrame:
    """Get report from provided data and similarity threshold."""
    lot_groupings = []
    for _, lot in data.iterrows():
        similar_objects = find_similar_objects(data, lot, similarity_threshold)
        avg_price_2017 = similar_objects[
            similar_objects.month_year == '2017_11'
            ]['price_usd'].mean()
        avg_price_2018 = similar_objects[
            similar_objects.month_year == '2018_03'
            ]['price_usd'].mean()
        if avg_price_2017 >= 0 and avg_price_2018 >= 0:
            grouping_id = similar_objects.sort_values('lot_number')['lot_number'].sum()
            metadata = similar_objects[['title', 'price_usd', 'height', 'width']].to_dict()
            grouping = {
                'artist': lot.artist_description,
                'grouping_id': grouping_id,
                'avg_price_2017_11': avg_price_2017,
                'avg_price_2018_03': avg_price_2018,
                'price_diff': (avg_price_2018 - avg_price_2017) / avg_price_2017,
                'metadata': metadata,
            }
            lot_groupings.append(grouping)
        else:
            pass
    return lot_groupings

if __name__ == '__main__':
    SIMILARITY_THRESHOLD = float(sys.argv[1])
    DATA = data_prep()
    LOT_GROUPINGS = get_report(DATA, SIMILARITY_THRESHOLD)
    LOT_GROUPINGS = pd.DataFrame(LOT_GROUPINGS).drop_duplicates('grouping_id')
    LOT_GROUPINGS.to_csv(config.REPORT_CSV)
