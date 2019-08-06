def get_buildings(zipcode):
    #IMPORT
    import pandas as pd
    # WRITE NOTIFICATION TO LOG
    print("Beginning to Query Occupied Housing Units")
    #READ CENSUS DATA
    buildings = pd.read_csv('/home/ec2-user/efs-mnt/data/ACS_17_5YR_S2504_with_ann.csv',
                        usecols=[1,3], skiprows = 1, dtype={'Id2':'object','Occupied housing units; Estimate; Occupied housing units':'object'})
    buildings.columns = ['zipcode','buildings']
    #FORMAT ZIPCODE
    buildings['zipcode']=buildings['zipcode'].str.zfill(5)
    #RETURN ROW THAT MATCHES REQUESTED ZIPCODE AS DICTIONARY
    results =  buildings[buildings['zipcode']==zipcode].to_dict('index')
    # PRINT TO LOG
    print(results)
    return results
