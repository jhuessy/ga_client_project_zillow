def get_citystate(zipcode):
    #IMPORT
    import pandas as pd
    #NOTIFICATION TO LOG
    print("Beginning to Query ZIPCode Location")
    #READ ZIPCODE LIST
    zipstate = pd.read_csv('/home/ec2-user/efs-mnt/data/zipstates.csv',error_bad_lines=False,warn_bad_lines=True,skiprows=10)
    zipstate = zipstate[['Zipcode','City','State']]
    #RETURN ROW FOR REQUESTED ZIPCODE
    results =  zipstate[zipstate['Zipcode']==zipcode].to_dict('index')
    #PRINT RESULTS TO LOG
    print(results)
    return results
