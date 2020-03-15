import settings

import requests, json, re, os
from pathlib import Path
import pandas as pd


def get_csv_urls():
    response = requests.get(settings.AIRBNB_DATA_LINKS)
    csv_str_list = re.findall(r'"http://.*.csv"', response.text)
    url_list = []
    # remove double quotes
    for csv_str in csv_str_list:
        url_list.append(csv_str[1:-1])
    return url_list


def get_listings_urls():
    url_list = get_csv_urls()
    listings_urls = []
     # fetch listings data only
    for url in url_list:
        try:
            filetype_match = re.search(r'http://data\.insideairbnb\.com/.*?/.*?/.*?/.*?/visualisations/(.*?).csv', url)
            filetype = filetype_match.groups()[0]
        except:
            print('Could not parse filetype')
            continue
        if filetype != 'listings':
            print(f'Not Listings file: {filetype}. Skipping...')
            continue
        else:
            listings_urls.append(url)
    return listings_urls


def import_all():
    # get urls with listings data
    url_list = get_listings_urls()
    url_list_len = len(url_list)
    print(f'{url_list_len} listings urls in list')
    
    # get list of previously pulled urls
    if os.path.exists(settings.URLS_USED_PATH):
        with open(settings.URLS_USED_PATH, 'r') as file:
            urls_used = json.load(file)
    else:
        urls_used = []
    print(urls_used)
    
    # maintain dict, ordering data by location
    median_prices = {}
    
    for url in url_list:
        print(f'\nChecking {url}')
        if url in urls_used:
            print(f'Data for URL has been used already: {url}. Skipping...')
            continue
        # get data from url
        try:
            df = pd.read_csv(url)
        except:
            print(f'Could not read_csv into dataframe from url: {url}')
            continue
            
        # retrieve location for data (country, region, city)
        # format of links: 'http://data.insideairbnb.com/{country}/{region}/{city}/{YYYY-MM-DD}/visualisations/{filename}.csv    
        try:
            country_match = re.search(r'http://data\.insideairbnb\.com/(.*?)/.*$', url)
            country = country_match.groups()[0]
            region_match = re.search(r'http://data\.insideairbnb\.com/.*?/(.*?)/.*$', url)
            region = region_match.groups()[0]
            city_match = re.search(r'http://data\.insideairbnb\.com/.*?/.*?/(.*?)/.*$', url)
            city = city_match.groups()[0]
            date_match = re.search(r'http://data\.insideairbnb\.com/.*?/.*?/.*?/(.*?)/.*$', url)
            date = date_match.groups()[0]
        except:
            print(f'Could not parse info from url: {url}')
        
        try:
            median_price = df.price.median()
        except:
            print('Could not get median from df:', df)
            continue

        # track that this URL has been analyzed
        urls_used.append(url)
        
        full_location = f'{country}_{region}_{city}'
        if full_location not in median_prices.keys():
            median_prices[full_location] = {}
        if date in median_prices[full_location]:
            print(f'{date} is already in dict for {full_location}')
            continue
        median_prices[full_location][date] = median_price
        print(f'Median price for {full_location}, {date}: {median_price}')

    # save data    
    with open(settings.MEDIAN_PRICES_PATH, 'w') as fp:
        json.dump(median_prices, fp)
    print(f'Saved median_prices as {fn}\n')

    with open(settings.URLS_USED_PATH, 'w') as fp:
        json.dump(urls_used, fp)
    print(f'Saved urls_used as {fn}')
    
    return median_prices


if __name__ == "__main__":
    import_all()