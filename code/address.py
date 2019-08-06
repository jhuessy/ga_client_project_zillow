def get_address(zipcode,state):
    #IMPORTS
    import pandas as pd
    import numpy as np
    import glob
    #READ ALL CSVS IN THE APPROPRIATE STATE FOLDER
    filepath = '/home/ec2-user/efs-mnt/data/us/'+state
    #CREATE GLOB OF FILENAMES
    all_files = glob.glob(filepath+'/*.csv')
    li = []
    #LET LOG KNOW WE ARE QUERYING ADDRESSES
    print("Beginning to Generate Address Sample...")
    #ITERATE OVER FILES
    for filename in all_files:
        #READ FILES
        datain = pd.read_csv(filename, index_col=None,header=0,dtype={'CITY': 'object',
            'DISTRICT': 'object',
            'HASH': 'object',
            'ID': 'object',
            'LAT': 'float64',
            'LON': 'float64',
            'NUMBER': 'object',
            'POSTCODE': 'object',
            'REGION': 'object',
            'STREET': 'object',
            'UNIT': 'object'})
        #APPEND FILES TO LIST
        li.append(datain)
    #CREATE DATAFRAME OF ALL ADDRESSES IN STATE
    df = pd.concat(li,axis=0,ignore_index=True)
    df.columns = ['LON', 'LAT', 'NUMBER', 'STREET', 'UNIT', 'CITY', 'DISTRICT', 'REGION', 'POSTCODE', 'ID', 'HASH']
    #SUBSET DATA FRAME TO ONLY ADDRESSES IN ZIPCODE
    df = df[df['POSTCODE']==zipcode]
    #IF THERE ARE FEWER THAN 100 ADDRESSES, USE THEM ALL, OTHERWISE SAMPLE 100
    length = df.shape[0]
    if length>100:
        sample_size=100
    else:
        sample_size=length
    results =df.sample(n=sample_size).to_dict('index')
    #OUTPUT SELECTED ADDRESSES TO LOG
    print(pd.DataFrame(results).T)
    #RETURN SELECTED ADDRESSES
    return results
