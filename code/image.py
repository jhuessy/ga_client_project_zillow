# coding: utf-8
def get_map(zipcode,zdf):
    import matplotlib
    matplotlib.use('Agg')
    # load required Python libraries
    from uszipcode import SearchEngine
    from bokeh.io import export_png,output_file, show
    from bokeh.models import ColumnDataSource, GMapOptions, LinearColorMapper,ColorBar,NumeralTickFormatter
    from bokeh.models.glyphs import Patch
    from bokeh.plotting import gmap
    from bokeh.embed import components
    from bokeh.transform import linear_cmap
    from bokeh.palettes import inferno

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    from babel.numbers import format_currency
    #WRITE NOTIFICATION TO LOG
    print("Beginning Map...")




    # ns/dsi8 - July 2019
    # Project 5 Team: N.Scott, J.Huessy, E.Stokes
    # Problem 4: Extracting Building Values from Zillow

    # this function accepts input arguments for zipcode and a dataframe (Zillow Zestimate data)
    # invoke SearchEngine for zipcode search
    search = SearchEngine(simple_zipcode=False)
    # pass a zipcode into search
    zipcode_data = search.by_zipcode(zipcode)
    # create a dictionary with retrieved details
    zip_dict = zipcode_data.to_dict()

    # get all longitudes, latitudes for specified zip
    zip_poly = zip_dict['polygon']
    # isolate all latitudes for specified zip
    zip_poly_lat = [poly[1] for poly in zip_poly]
    # isolate all longitudes for specified zip
    zip_poly_lng = [poly[0] for poly in zip_poly]

    # define zipcode border (latitude & longitude)
    zip_dict_gmap_lat = zip_dict['lat']
    zip_dict_gmap_lng = zip_dict['lng']
    zip_dict_zipcode = zip_dict['zipcode']

    zest_total = zdf['price'].sum()
    zest_dollar = format_currency(zest_total, 'USD', locale='en_US')

    # output filename includes zipcode
    #filename2 = f'''ZIP_{zip_dict_zipcode}_gmap.html'''

    # mapping options based on Bokeh documentation
    # https://bokeh.pydata.org/en/latest/docs/reference/models/map_plots.html#bokeh.models.map_plots.GMapOptions
    map_options = GMapOptions(lat=zip_dict_gmap_lat, lng=zip_dict_gmap_lng, map_type="roadmap", zoom=11)

    # For GMaps to function, Google requires you obtain and enable an API key:
    # https://developers.google.com/maps/documentation/javascript/get-api-key
    # Replace the value below with your personal API key:
    # p = gmap("GOOGLE_API_KEY", map_options, title="Austin")

    # map title includes zipcode and TOTAL Zillow "Zestimate" value for specified zipcode
    p = gmap("", map_options)
    #, title=f'''ZIPCODE:  {zip_dict_zipcode} ----> Zestimate TOTAL:  {zest_dollar}''')

    # based on code from Boston DSI cohort - Jan 2019
    source = ColumnDataSource(
        data = dict(
            lat=zip_poly_lat,
            lon=zip_poly_lng))

    patch = Patch(x='lon', y='lat', fill_color="blue", fill_alpha=0.08)
    p.add_glyph(source, patch)

    #ADDING SCATTERPLOT TO MAP
    #CREATE COLUMN DATA SOURCE FROM ZIPCODE DATAFRAME
    x = zdf['long']
    y = zdf['lat']
    z = zdf['price']
    source = ColumnDataSource(dict(x=x,y=y,z=z))
    #CREATE COLOR MAPPER FROM PRICE COLUMN
    mapper = linear_cmap(field_name='z', palette=inferno(256) ,low=min(z) ,high=max(z))
    #ADD CIRCLES AT EACH LAT/LONG PAIR COLOR-CODED BY PRICE
    p.circle(x='x', y='y', line_color='black',
       color=mapper, fill_alpha=1, size=5, source=source)
       #CURRENCY FORMAT FOR TICKS
    formatter = NumeralTickFormatter(format='$0,0.00')
    #ADD COLORBAR LEGEND
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8,formatter=formatter,  location=(0,0))
    p.add_layout(color_bar, 'right')
    # CREATE HTML/JAVASCRIPT COMPONENTS OF BOKEH PLOT
    script,div = components(p)
    return script,div

def get_hist(zipcode,zdf, buildings):
    #WRITE NOTIFICATION TO LOG
    print("Beginning Histogram Plot...")
    #IMPORTS
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    import seaborn as sns
    import numpy as np
    #CREATE PLOT
    fig, ax = plt.subplots(figsize=(9,3 ))
    #ADD QUERY DATA TO PLOT
    sns_plot = sns.distplot(zdf['price'],kde=False,color='green',label ='Zillow Estimates')
    #CREATED IMPUTED DATASET FROM LOG NORMAL DISTRIBUTION
    mu = np.log(zdf['price']).mean()
    sigma = np.std(np.log(zdf['price']))
    impute = np.exp(np.random.normal(mu,sigma,buildings))
    #ADD IMPUTED DATA TO PLOT
    sns_plot = sns.distplot(impute,kde=False,color='orange',label='Imputed Prices')
    #MAKE PLOT FIT CANVAS BETTER
    fig.tight_layout()
    #CURRENCY FORMAT FOR TICKS
    fmt = '${x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.xaxis.set_major_formatter(tick)
    # ADD LEGEND
    ax.legend()
    # ADD X LABEL
    sns_plot.set_xlabel("Estimated Price")
    #CREATE FIGURE OBJECT
    sns_fig = sns_plot.get_figure()
    #SAVE FIGURE OBJECT
    filename = "static/imgs/hist.jpg"
    sns_fig.savefig(filename)
    return filename
