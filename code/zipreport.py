def get_report(zipcode):
    #IMPORTS
    import requests
    import time
    from xml.etree import ElementTree as ET
    import pandas as pd
    from address import get_address
    from buildings import get_buildings
    from citystate import get_citystate
    from image import get_hist,get_map
    import matplotlib
    #WRITE NOTIFICATION TO LOG
    print("Beginning Query...")
    #START TIMER
    ts=time.time()
    #GET BUILDINGS DATA
    buildingsdf = pd.DataFrame(get_buildings(zipcode)).T
    buildings = int(buildingsdf['buildings'].values[0])
    #GET CITY STATE DATA
    statedf = pd.DataFrame(get_citystate(int(zipcode))).T
    state = statedf['State'].values[0].lower()
    #CREATE EMPTY PRICE ESTIMATE LIST
    zestimatelist =[]
    # GET LIST OF ADDRESSES
    result =get_address(zipcode,state)
    #WRITE NOTIFICATION TO LOG
    print("Beginning Zillow Query...")
    #BEGIN LIST OF FAILED QUERIES
    print("The following addresses failed to return results from Zillow")
    #ITERATE OVER ADDRESSES
    for key in result.keys():
        #QUERY ZILLOW FOR THE GIVEN ADDRESS
        zbase_url="http://www.zillow.com/webservice/GetSearchResults.htm"
        zparams={
            'zws-id':'',
            'citystatezip':str(result[key]['CITY'])+','+state,
            'address':str(result[key]['NUMBER'])+' '+str(result[key]['STREET'])
        }
        zreq=requests.get(zbase_url,params=zparams)
        #PARSE XML
        root=ET.fromstring(zreq.content)
        #PULL PRICE, LATITUDE AND LONGITUDE FROM THE QUERY RESULTS
        try: 
            zestimatelist.append({'price':root.findall('./response/results/result/zestimate/amount')[0].text,
                                  'lat':root.findall('./response/results/result/address/latitude')[0].text,
                                  'long':root.findall('./response/results/result/address/longitude')[0].text
                                 })
        except:
            #WRITE FAILED QUERIES TO LOG
            print('no data',zparams['citystatezip'],zparams['address'])
    #CONVERT PRICE ESTIMATE LIST TO DATAFRAME AND CONVERT COLUMNS TO NUMERIC
    zdf = pd.DataFrame(zestimatelist)
    zdf['lat'] = pd.to_numeric(zdf['lat'], errors='coerce')
    zdf['long'] = pd.to_numeric(zdf['long'], errors='coerce')
    zdf['price'] = pd.to_numeric(zdf['price'], errors='coerce')
    #DROP NULL ROWS
    zdf.dropna(inplace=True)
    prices = pd.to_numeric(zdf['price'],errors='coerce')
    #GET HISTOGRAM
    get_hist(zipcode,zdf,buildings)
    #GET MAP
    script,div =get_map(zipcode,zdf)
    #CREATE HTML OUTPUT FOR STATS TABLE
    results = '<div><h2>Residential Property Values for '+zipcode+'</h2><br><table border="1" id="myTable" width="100%" style="table-layout: initial;"><tr><td>Mean Property Value</td><td>$'+str('{:,}'.format(round(prices.mean(),2)))+'</td></tr>'\
              '<tr><td> Median Property Value</td><td>$'+str('{:,}'.format(round(prices.median(),2)))+'</td></tr>'\
              '<tr><td> Minimum Property Value</td><td>$'+str('{:,}'.format(round(prices.min(),2)))+'</td></tr>'\
              '<tr><td> Maximum Property Value</td><td>$'+str('{:,}'.format(round(prices.max(),2)))+'</td></tr>'\
              '<tr><td> Total Estimated Property Value</td><td>$'+str('{:,}'.format(round(prices.sum()*buildings/100,2)))+'</td></tr></table><br>'\
              '<h2>Distribution of Zillow Estimates</h2>'
    #PRINT EXECUTION TIME
    print("Time to execute was:")
    print time.time()-ts
    return results,script,div
