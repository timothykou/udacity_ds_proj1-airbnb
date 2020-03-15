import import_median_prices, settings

import json, os
import pandas as pd
import plotly.graph_objects as go


# gets saved median prices 
def get_median_prices():
    if not os.path.exists(settings.MEDIAN_PRICES_PATH):
        import_median_prices.import_all()
    try:
        with open(settings.MEDIAN_PRICES_PATH, 'r') as file:
            median_prices = json.load(file)
    except:
        print(f'Could not load median prices json file from {settings.MEDIAN_PRICES_PATH}')
    return median_prices


def plot_prices():
    median_prices = get_median_prices()
    # each location's median price data is one column in a df
    df = pd.DataFrame()
    for location, location_d in median_prices.items():
        # create df for this location
        dff = pd.DataFrame(location_d, index=[location]).T
        # check for errors by excluding locations if any median price > 5k (could be small dataset)
        if (dff[location] > 5000).any():
            print(f'Excluding {location} - at least one median price > $5k / night')
            continue
        # remove small datasets - less than 10 dates
        if len(dff) < 10:
            print(f'Excluding {location} - less than 10 data points')
            continue
        # add new location as column
        df = pd.concat([df, dff], axis=1, join='outer')

    df.sort_index(axis=1, inplace=True)
    print(df)
    # graph prices for each location
    fig = go.Figure()
    
    # iterate through locations and add line for each
    for location in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[location],
                    mode='lines+markers',
                    name=location))
    fig.show()
    return fig


if __name__ == "__main__":
    plot_prices()